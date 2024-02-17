from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import vamtoolbox as vam
import torch
import torch.nn as nn
import os
import io
import pickle



def scale_to_fit(image_normalized, desired_height, desired_width):
    # Calculate the aspect ratio of the original image
    original_height, original_width = image_normalized.shape
    original_aspect_ratio = original_width / original_height
    desired_aspect_ratio = desired_width / desired_height

    if original_aspect_ratio > desired_aspect_ratio:
        # scale image_normalized so that the width = desired_width
        scaled_width = desired_width
        scaled_height = int(desired_width / original_aspect_ratio)
        scaled_image = cv2.resize(image_normalized, (scaled_width, scaled_height))
        buffer_image = np.zeros((desired_height, desired_width))
        start_y = (desired_height - scaled_height) // 2
        buffer_image[start_y:start_y+scaled_height, :] = scaled_image
    else:
        # scale image_normalized so that the height = desired_height
        scaled_height = desired_height
        scaled_width = int(desired_height * original_aspect_ratio)
        scaled_image = cv2.resize(image_normalized, (scaled_width, scaled_height))
        buffer_image = np.zeros((desired_height, desired_width))
        start_x = (desired_width - scaled_width) // 2
        buffer_image[:, start_x:start_x+scaled_width] = scaled_image
    return buffer_image


def saveProjections(b, dimension, save_dir: str, image_prefix: str = "image", image_type: str = ".png"):
    for k in range(len(b[0, :, 0])):
        save_path = os.path.join(save_dir, f"{image_prefix}{str(k).zfill(4)}{image_type}")
        print(f"save path = {save_path}")
        image = b[:, k, :]

        # Normalize the pixel values to the range [0, 255]
        image_normalized = (image - image.min()) * (255.0 / (image.max() - image.min()))

        # Calculate the desired dimensions with black buffer
        desired_height = dimension[0]
        desired_width = dimension[1]

        buffer_image = scale_to_fit(image_normalized, desired_height, desired_width)

        # Convert to integer type and create the image
        buffer_image = buffer_image.astype(np.uint8)
        im = Image.fromarray(buffer_image)

        im.save(save_path, subsampling=0, quality=100)
        # print(f"Saving image {str(k).zfill(4)}/{str(len(b[0])).zfill(4)}")

class Options:

    __default_FBP = {"offset":False}
    __default_CAL = {"learning_rate":0.01,"momentum":0,"positivity":0,"sigmoid":0.01}
    __default_PM = {"rho_1":1,"rho_2":1,"p":1}
    __default_OSMO = {"inhibition":0}

    def __init__(self,method : str ='CAL',n_iter : int = 50,d_h : float = 0.8,d_l : float = 0.7,filter : str ='ram-lak',units:str='normalized',**kwargs):
        """
        Parameters
        ----------

        method : str
            Type of VAM method
                - "FBP"
                - "CAL"
                - "PM"
                - "OSMO"
        
        n_iter : int
            number of iterations to perform

        d_h : float
            in-target dose constraint

        d_l : float
            out-of-target dose constraint

        filter : str
            filter for initialization ("ram-lak", "shepp-logan", "cosine", "hamming", "hanning", None)

        learning_rate : float, optional (CAL)
            step size in approximate gradient descent
        
        momentum : float, optional (CAL)
            descent momentum for faster convergence

        positivity : float, optional (CAL)
            positivity constraint enforced at each iteration
        
        sigmoid : float, optional (CAL)
            sigmoid thresholding strength
        
        rho_1 : float, optional (PM)

        rho_2 : float, optional (PM)

        p : int, optional (PM)

        inhibition : float, optional (OSMO)




        """
        self.method = method
        self.n_iter = n_iter
        self.d_h = d_h
        self.d_l = d_l
        self.filter = filter
        self.units = units
        self.__default_FBP.update(kwargs)
        self.__default_CAL.update(kwargs)
        self.__default_PM.update(kwargs)
        self.__default_OSMO.update(kwargs)
        self.__dict__.update(kwargs)  # Store all the extra variables

        self.verbose = self.__dict__.get('verbose',False)
        self.bit_depth = self.__dict__.get('bit_depth',None)
        self.exit_param = self.__dict__.get('exit_param',None)

        if method == "FBP":
            self.offset = self.__default_FBP["offset"]

        if method == "CAL":
            self.learning_rate = self.__default_CAL["learning_rate"]
            self.momentum = self.__default_CAL["momentum"]
            self.positivity = self.__default_CAL["positivity"]
            self.sigmoid = self.__default_CAL["sigmoid"]

        if method == "PM":
            self.rho_1 = self.__default_PM["rho_1"]
            self.rho_2 = self.__default_PM["rho_2"]    
            self.p = self.__default_PM["p"]        

        if method == "OSMO":
            self.inhibition = self.__default_OSMO["inhibition"]

def returnPreOptimize(target_geo : vam.geometry.TargetGeometry,proj_geo : vam.geometry.ProjectionGeometry,options:Options):
    if options.units != "normalized" or proj_geo.absorption_coeff is not None:
        proj_geo.calcAbsorptionMask(target_geo)

    if options.method == "OSMO":
        A = vam.projectorconstructor.projectorconstructor(target_geo,proj_geo)
        
        # the first model is just the target
        x_model = np.copy(target_geo.array) 



        target_filtered = vam.util.data.filterTargetOSMO(target_geo.array,options.filter)
        x_model = np.real(target_filtered)

        # the initial sinogram is just the forward projection of the model
        b = A.forward(x_model)
        b = np.clip(b,0,None)
        # x = A.backward(b)
        # x = x/np.amax(x)
        return b
    
def generatedata(dir_list, resolution, angles, optimizer_params, dimension, OutputFolder, PreProjectionFolder):
    for i in range(len(dir_list)):
        print("optimizing: " + dir_list[i])
        targetgeo = vam.geometry.TargetGeometry(stlfilename=dir_list[i], resolution=resolution)
        
        # targetgeo.show()

        # Set output name to match the STL input file
        OutputPrefix = os.path.splitext(os.path.split(dir_list[i])[1])[0]
        print(os.path.split(dir_list[i]))

        # Can we put this in calculated settings?
        proj_geo = vam.geometry.ProjectionGeometry(angles, ray_type='parallel', CUDA=True)

        b = returnPreOptimize(targetgeo, proj_geo, optimizer_params)
        opt_sino, opt_recon, error = vam.optimize.optimize(targetgeo, proj_geo, optimizer_params)

        opt_sino.show()
        opt_recon.show()
        slice_2d = b[:, 180, :].T  # Selecting the first 100 rows from the second dimension
        plt.imshow(slice_2d)
        plt.colorbar()  # Optional: Add a colorbar to the plot
        plt.show()

        # Resize opt_sino.array with black buffer
        # desired_height = dimension[0]
        # desired_width = dimension[1]
        
        # Save images
        print("output folder:", OutputFolder)
        print("output prefix:", OutputPrefix)
        saveProjections(b, dimension, save_dir=OutputFolder, image_prefix=OutputPrefix)
        saveProjections(opt_sino.array, dimension, save_dir=PreProjectionFolder, image_prefix=OutputPrefix)
        # print("sino size:" + str(opt_sino.array.shape))
        del targetgeo
        del proj_geo
        del b
        del opt_sino
        del opt_recon
        del slice_2d

########################################################################
# AI part
########################################################################



class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU()
        )

        self.middle_conv = nn.Sequential(
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
        )

        self.decoder = nn.Sequential(
            
            nn.Conv2d(192, 64, kernel_size=3, padding=1),  # Concatenating feature maps from the encoder
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 1, kernel_size=1)
        )

    def forward(self, x):
        encoder_output1 = self.encoder(x)
        encoder_output2 = self.middle_conv(encoder_output1)
        decoder_input = torch.cat([encoder_output2, encoder_output1], dim=1)  # Concatenate feature maps
        decoder_output = self.decoder(decoder_input)
        return decoder_output
  
    
class DropoutUNet(nn.Module):
    def __init__(self, dropout_prob=0.5):
        super(DropoutUNet, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob)
        )

        self.middle_conv = nn.Sequential(
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
        )

        self.decoder = nn.Sequential(
            nn.Conv2d(192, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Dropout2d(dropout_prob),
            nn.Conv2d(64, 1, kernel_size=1)
        )

    def forward(self, x):
        encoder_output1 = self.encoder(x)
        encoder_output2 = self.middle_conv(encoder_output1)
        decoder_input = torch.cat([encoder_output2, encoder_output1], dim=1)
        decoder_output = self.decoder(decoder_input)
        return decoder_output



# Function to load grayscale images from a folder
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
    return images

def generatedata_ML(model_path, pre_optimization_folder, OutputFolder, batch_size, use_cpu = False):

    model_buffer = io.BytesIO(open(model_path, 'rb').read())
    model = DropoutUNet()
    if use_cpu:
        model.load_state_dict(torch.load(model_buffer, map_location=torch.device('cpu')))
    else:
        model.load_state_dict(torch.load(model_buffer))
    model.eval()
    
    # Load pre-optimization grayscale images
    pre_optimization_images = load_images_from_folder(pre_optimization_folder)

    # Convert image lists to numpy arrays
    pre_optimization_images = np.array(pre_optimization_images)

    # Normalize the image data
    pre_optimization_images = pre_optimization_images / 255.0

    # Convert numpy arrays to PyTorch tensors
    x_train = torch.from_numpy(pre_optimization_images).unsqueeze(1).float()

    
    device_count = torch.cuda.device_count()
    if device_count > 0:
        print("Available GPUs:")
        for i in range(device_count):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("No GPUs available. PyTorch is using CPU.")

    # Set the device (CPU or GPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if torch.cuda.is_available():
        model = model.to(device)
        print("PyTorch is using GPU.")
    else:
        print("PyTorch is using CPU.")

    # Convert the data to the appropriate device
    x_train = x_train.to(device)

    # Create a directory to save the output images
    if not os.path.exists(OutputFolder):
        os.makedirs(OutputFolder)

    # Function to save grayscale images
    def save_images(images, path, prefix="output_", file_extension=".png"):
        for i, image in enumerate(images):
            filename = os.path.join(path, f"{prefix}{i:04d}{file_extension}")
            cv2.imwrite(filename, (image * 255).astype(np.uint8))

    # Create an empty list to store the output images
    output_images = []

    # Iterate through your input images in batches
    for i in range(0, len(x_train), batch_size):
        batch = x_train[i:i + batch_size]
        
        # Make predictions using the U-Net model
        with torch.no_grad():
            predicted_images = model(batch)

        # Convert the predicted images back to NumPy arrays
        predicted_images = predicted_images.squeeze(1).cpu().numpy()

        # Append the predicted images to the list
        output_images.extend(predicted_images)

    # Save the output images
    save_images(output_images, OutputFolder)





    
################################################################
# Accuracy measurenment
################################################################
from scipy.ndimage import zoom

def load_png_to_numpy_array(folder_path, rotate=False):

    print(f"loading images from folder {folder_path}")

    image_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(folder_path, filename))
            image_list.append(np.array(img))


    # image_list = image_list[::-1] # images are flipped like in a mirror so we un-flip them
    images_array = np.array(image_list)

    if rotate:
        # Rotate every image in the array by 90 degrees
        rotated_images_array = np.array([np.rot90(img) for img in images_array])


    plt.imshow(rotated_images_array[0])
    plt.axis('off')  # Turn off axis labels and ticks
    plt.show()
    print("showing first loaded image")
    return rotated_images_array


def expand_3d_numpy_array(original_array, target_shape):
    

    # Assuming your original 3D array is called original_array with shape (115, 115, 128)
    original_shape = original_array.shape

    

    # Calculate the scaling factors for each dimension
    scaling_factors = (
        target_shape[0] / original_shape[0],
        target_shape[1] / original_shape[1],
        target_shape[2] / original_shape[2]
    )

    # Use the zoom function to interpolate the original array to the target shape
    interpolated_array = zoom(original_array, zoom=scaling_factors, order=1)
    return interpolated_array

def inverse_radon(projections, STLfile_name, resolution):
    num_angles = 360
    angles = np.linspace(0, 360 - 360 / num_angles, num_angles)
    proj_geo = vam.geometry.ProjectionGeometry(angles,ray_type='parallel',CUDA=True)
    target_geo = vam.geometry.TargetGeometry(stlfilename=STLfile_name, resolution=resolution)

    # Define the target shape (128, 128, 128)
    dims = projections.shape
    target_shape = (dims[1], dims[1], dims[2])
    target_geo.array = expand_3d_numpy_array(target_geo.array, target_shape)
    
    target_geo.nX = target_shape[0]
    target_geo.nY = target_shape[1]
    # projections = projections[::-1]


    from vamtoolbox.projector.Projector3DParallelCUDA import Projector3DParallelCUDAAstra
    A = Projector3DParallelCUDAAstra(target_geo,proj_geo)
    tmp_projections = np.transpose(projections,(2,0,1))

    x = A.backward(tmp_projections)
    x = x/np.amax(x) # normalize

    # print(f"x shape : {x.shape}")

    # _error = vam.metrics.calcVER(target_geo,x)
    return x

# DEFINE ERROR FUNCTIONS HERE

d_l = 0.6
d_h = 0.85

def squared_difference(array1, array2):
    return (array1 - array2) ** 2

def MSE(array1, array2):
    squared_diff = squared_difference(array1, array2)
    mse = squared_diff.mean()
    return mse

def zero(array1, array2):
    return 0

def fourth(array1, array2):
    fourth_diff = abs((array1 - array2) ** 3)
    return fourth_diff.mean()

def CUBED(array1, array2):
    cubed_diff = abs((array1 - array2) ** 3)
    return cubed_diff.mean()

def round_3d_array(array, round_down_threshold, round_up_threshold):
    rounded_array = [[[0 if value <= round_down_threshold else 1 if value >= round_up_threshold else 2 for value in row] for row in plane] for plane in array]
    return np.array(rounded_array)

def L1_dif(array1, array2):
    # Calculate the L1 norm (sum of absolute differences)
    l1_norm = np.sum(np.abs(array1 - array2))
    return l1_norm

def total_dose_dif(array1, array2):
    # Calculate the L1 norm (sum of absolute differences)
    return abs(np.sum(array1) - np.sum(array2))
    

def count_above_dif_threshold(array1, array2, threshold = 0.2):
    # Calculate absolute differences between the two arrays
    abs_diff = np.abs(array1 - array2)
    
    # Create a mask where values are above the threshold
    above_threshold_mask = abs_diff > threshold
    
    # Use the mask to filter the absolute differences and then sum them
    return np.sum(above_threshold_mask)


# dif = squared_difference(reconstruction_ML, ground_truth)

def compare(array1, array2):
    
    mse = MSE(array1, array2)
    l1 = L1_dif(array1, array2)

    threshold = 0.1
    count = count_above_dif_threshold(array1, array2, threshold)

    array2_descretized = np.array(round_3d_array(array2, round_down_threshold=d_l, round_up_threshold=d_h))

    solidified_voxel_differences = count_above_dif_threshold(array1, array2, threshold)

    # calcualte percentage eerors assuming array1 an darray2 have same number of voxels
    total_pixels = array1.shape[0] * array1.shape[1] * array1.shape[2]

    print(f"MSE: {mse}, L1: {l1}, % of different voxels above {threshold}: {count/total_pixels} solidified voxel difference to STL: {solidified_voxel_differences}")


# """
# find voxels of value VALUE that are neighbors with voxels that dont  have value VAUE
# """
# def find_border_voxels(arr, value):
#     # Create an array to store the neighboring offsets
#     neighbor_offsets = np.array([
#         [-1, 0, 0], [1, 0, 0],
#         [0, -1, 0], [0, 1, 0],
#         [0, 0, -1], [0, 0, 1]
#     ])

#     adjacent_voxels = []

#     # Iterate through the 3D array
#     for z in range(arr.shape[0]):
#         for x in range(arr.shape[1]):
#             for y in range(arr.shape[2]):
#                 if arr[z, x, y] == value:
#                     # Check neighboring voxels
#                     for offset in neighbor_offsets:
#                         nz, nx, ny = z + offset[0], x + offset[1], y + offset[2]
#                         if (
#                             0 <= nz < arr.shape[0] and
#                             0 <= nx < arr.shape[1] and
#                             0 <= ny < arr.shape[2] and
#                             arr[nz, nx, ny] != value
#                         ):
#                             adjacent_voxels.append((z, x, y))
#                             break  # No need to check other neighbors

#     return adjacent_voxels
def find_border_voxels(arr, value):
    # Create an array to store the neighboring offsets
    neighbor_offsets = np.array([
        [-1, 0, 0], [1, 0, 0],
        [0, -1, 0], [0, 1, 0],
        [0, 0, -1], [0, 0, 1]
    ])

    # Find indices of voxels with the specified value
    value_indices = np.column_stack(np.where(arr == value))

    # Find indices of neighboring voxels without the specified value
    neighbor_indices = []

    # print("looking in", value_indices)

    for idx in value_indices:
        add = False
        for offset in neighbor_offsets:
            new_idx = tuple(idx + offset)
            within_bounds = all(0 <= i < dim for i, dim in zip(new_idx, arr.shape))
            if within_bounds and arr[new_idx] != value:
                add = True
        
        if add:
            neighbor_indices.append(tuple(idx))
                
    return neighbor_indices




#TODO: change the dijkstras if possible for more accurate distance priorities
from collections import deque
"""
performs bfs starting at start_point on space array. Stops when it seems a voxel with float_value
"""
def bfs_search(float_value, start_point, space_array, max_distance = 3):
    # Define the 6 possible movement directions in 3D space
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    # Create a set to keep track of visited coordinates
    visited = set()

    # Create a queue for BFS with the starting point and depth
    queue = deque([(start_point, 0)])

    while queue:
        current_point, depth = queue.popleft()

        # Check if the current point has the desired float value
        if space_array[current_point] == float_value:
            return current_point
        
        # check if we should give up on finding the point
        if depth >= max_distance:
            return (0,0,4096) + start_point
            # return current_point

        # Mark the current point as visited
        visited.add(current_point)

        # Expand to neighboring coordinates
        for direction in directions:
            new_point = tuple(np.add(current_point, direction))

            # Check if the new point is within the space boundaries
            if all(0 <= i < dim for i, dim in zip(new_point, space_array.shape)) and new_point not in visited:
                queue.append((new_point, depth + 1))

    # If the desired value is not found, return None
    return None

import math
"""
returns l2 norm of 3d tuples (voxels)
"""
def l2norm(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2 + (x[2] - y[2])**2)


"""
MAKE SURE TO ROUND THE GROUND TRUTH AND RECONSTRUCTIONS so that solid voxels are 1.0, empty voxels are 0.0 nd in between is not counted

NOTE: The comparison does NOT include corners as borders.
i.e. 
[[1,2],
[3,4]]
means 1 is on border of 2 and 3, but is not a neighbor of 4
"""
def surface_compare(ground_truth_cured_surface, ground_truth_uncured_surface, reconstruction, multithreaded=True):
    
    print(f"finding bfs of border voxels... {len(ground_truth_cured_surface)}")
    if multithreaded:
        cured_voxel_error = sum(bfs_search_c(1, ground_truth_cured_surface, reconstruction))
    else:
        reconstruction_surface_mapping = [bfs_search(1, surface_voxel, reconstruction) for surface_voxel in ground_truth_cured_surface]
        print("done finding bfs of border voxels...")
        
        # sum the error
        cured_voxel_error = 0
        for i in range(len(ground_truth_cured_surface)):
            cured_voxel_error += l2norm(ground_truth_cured_surface[i], reconstruction_surface_mapping[i])

    
    print(f"finding bfs of border voxels... {len(ground_truth_uncured_surface)}")
    if multithreaded:
        uncured_voxel_error = sum(bfs_search_c(0, ground_truth_uncured_surface, reconstruction))
    else:
        reconstruction_uncured_surface_mapping = [bfs_search(0, surface_voxel, reconstruction) for surface_voxel in ground_truth_uncured_surface]
        print("done finding bfs of border voxels...")
    
        # sum the error
        uncured_voxel_error = 0
        for i in range(len(ground_truth_uncured_surface)):
            uncured_voxel_error += l2norm(ground_truth_uncured_surface[i], reconstruction_uncured_surface_mapping[i])
    
    return cured_voxel_error, uncured_voxel_error
    

def surface_compare_combined_error(ground_truth_cured_surface, ground_truth_uncured_surface, reconstruction):
    
    return sum(surface_compare(ground_truth_cured_surface, ground_truth_uncured_surface, reconstruction))


import matplotlib.pyplot as plt
from tqdm import tqdm
# Calculate optimal rotations

import vedo
    
def plot(data, d_l=0.1, d_h=1):
    vol = vedo.Volume(data).legosurface(vmin=d_l,vmax=d_h)
    vol.show(viewup="x")

def calculate_optimal_rotations_surface_compare(ground_truth, predicted, max_iterations=5, initial_range=[0, 4], resolution=5, name="undefined", print_errors = False):
    best_error = float('inf')
    best_rotations = 0
    error = []
    rotations_number = []
    print("processing ground truth")
    ground_truth = round_3d_array(ground_truth, round_down_threshold = 0.6, round_up_threshold = 0.85)
    
    
    print(f"finding border voxels...")
    ground_truth_cured_surface = find_border_voxels(ground_truth, 1) # gets a list of voxel coordinates on the surface (cured)
    ground_truth_uncured_surface = find_border_voxels(ground_truth, 0) # gets a list of voxel coordinates on the surface (cured)
    print("done finding border voxels...")

    for iteration in range(max_iterations):
        # Sample 'resolution' number of points in the interval 'initial_range'
        step_size = (initial_range[1] - initial_range[0]) / (resolution - 1)
        print(f"checking {initial_range[0]} to {initial_range[1]}")
        for i in range(resolution):
            temp = (initial_range[0] + i * step_size) * predicted
            temp = round_3d_array(temp, round_down_threshold = 0.6, round_up_threshold = 0.85)

            # calculate the error
            if not (temp == 0).any():
                error.append(np.inf)
            elif not (temp == 1).any():
                error.append(np.inf)
            else:
                print(ground_truth_uncured_surface)
                error.append(surface_compare_combined_error(ground_truth_cured_surface,  ground_truth_uncured_surface, temp))
            
            if print_errors:
                print(f"error at {(initial_range[0] + i * step_size)} is {error[-1]}")
            rotations_number.append((initial_range[0] + i * step_size))

        # Find the index of the minimum error in the current window
        min_error_idx = error.index(min(error))

        # Update the best error and rotations
        if error[min_error_idx] < best_error:
            best_error = error[min_error_idx]
            best_rotations = rotations_number[min_error_idx]

        # Update the search window for the next iteration
        # Ensure the range is centered around the minimum error point
        center = rotations_number[min_error_idx]
        width = (initial_range[1] - initial_range[0]) / 4
        initial_range = [center - width, center + width]

    # Create a figure and plot all data points
    sorted_lists = zip(rotations_number, error)
    sorted_lists = sorted(sorted_lists, key=lambda x: x[0])
    rotations_number, error = zip(*sorted_lists)
    plt.figure(figsize=(10, 6))
    plt.plot(rotations_number, error, marker='o')
    plt.title(f'Error vs. Rotation Factor for {name}')
    plt.xlabel('Rotation Factor')
    plt.ylabel('Error')
    plt.grid(True)

    plt.axvline(x=best_rotations, color='r', linestyle='--', label='Minimum Error')

    plt.legend()
    plt.show()

    return best_rotations


# use for non-surface compare funcitons
def calculate_optimal_rotations(ground_truth, predicted, error_function, max_iterations=5, initial_range=[0, 4], resolution=5, name="undefined", print_errors = True):
    best_error = float('inf')
    best_rotations = 0
    error = []
    rotations_number = []

    for iteration in range(max_iterations):
        # Sample 'resolution' number of points in the interval 'initial_range'
        step_size = (initial_range[1] - initial_range[0]) / (resolution - 1)
        print(f"checking {initial_range[0]} to {initial_range[1]}")
        for i in range(resolution):
            rotation = initial_range[0] + i * step_size
            print("Trying rotation: " + str(rotation))

            temp = rotation * predicted

            if rotation in rotations_number:   # Prevents some slow repeat calculations
                print("Error for this value of rotation already found!")
                error_value = error[rotations_number.index(rotation)]
            else:
                error_value = error_function(ground_truth, temp)
                # print("is temp fucked", rotation)
                if type(error_value == int):
                    error.append(error_value)
                else:
                    error.append(sum(sum(sum(error_value))))
                rotations_number.append(rotation)
            

            if print_errors:
                print(f"error at {rotation} is {error[rotations_number.index(rotation)]}")

        # Find the index of the minimum error in the current window
        min_error_idx = error.index(min(error))

        # Update the best error and rotations
        if error[min_error_idx] < best_error:
            best_error = error[min_error_idx]
            best_rotations = rotations_number[min_error_idx]

        # Update the search window for the next iteration
        # Ensure the range is centered around the minimum error point
        center = rotations_number[min_error_idx]
        width = (initial_range[1] - initial_range[0]) / 4
        initial_range = [center - width, center + width]

    # Create a figure and plot all data points
    sorted_lists = zip(rotations_number, error)
    sorted_lists = sorted(sorted_lists, key=lambda x: x[0])
    rotations_number, error = zip(*sorted_lists)
    plt.figure(figsize=(10, 6))
    plt.plot(rotations_number, error, marker='o')
    plt.title(f'Error vs. Rotation Factor for {name}')
    plt.xlabel('Rotation Factor')
    plt.ylabel('Error')
    plt.grid(True)

    plt.axvline(x=best_rotations, color='r', linestyle='--', label='Minimum Error')

    plt.legend()
    plt.show()

    return best_rotations
            
        


from stl import mesh

def rotate_stl(input_filename, output_filename):
      # Load the STL file
    mesh_data = mesh.Mesh.from_file(input_filename)

    # Get the vertices of the mesh
    vertices = mesh_data.vectors.reshape(-1, 3)

    # Calculate the bounding box of the mesh
    min_coords, max_coords = np.min(vertices, axis=0), np.max(vertices, axis=0)
    dimensions = max_coords - min_coords

    # Determine the axis along which the longest dimension lies
    longest_axis = np.argmax(dimensions)

    # Rotate the mesh so that the longest side faces upwards
    if longest_axis == 0:  # X-axis is the longest
        rotation_axis = np.array([0.0, 0.0, 1.0])
        rotation_angle = np.pi / 2
        mesh_data.rotate(rotation_axis, rotation_angle)
        rotation_axis = np.array([0.0, 1.0, -1.0])
        rotation_angle = np.pi
    elif longest_axis == 1:  # Y-axis is the longest
        rotation_axis = np.array([0.0, 1.0, -1.0])
        rotation_angle = np.pi
    else:  # Z-axis is the longest (no rotation needed)
        rotation_axis = np.array([0.0, 0.0, 0.0])
        rotation_angle = 0

    # Rotate the mesh around the selected axis
    mesh_data.rotate(rotation_axis, rotation_angle)

    # Calculate center after rotation
    newVertices = mesh_data.vectors.reshape(-1, 3)
    newMin, newMax = np.min(newVertices, axis=0), np.max(newVertices, axis=0)
    newCenter = (newMax + newMin)/2


    # Calculate the translation needed to recenter the mesh
    translation = -(newCenter)


    # Translate the mesh to recenter it
    mesh_data.x +=translation[0]
    mesh_data.y +=translation[1]
    mesh_data.z +=translation[2]

    # Save the rotated and recentered mesh to the output file
    mesh_data.save(output_filename)

def batch_rotate_stl_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all STL files in the input folder
    stl_files = [f for f in os.listdir(input_folder) if f.endswith('.stl')]

    for stl_file in stl_files:
        input_path = os.path.join(input_folder, stl_file)
        output_path = os.path.join(output_folder, stl_file)
        rotate_stl(input_path, output_path)
        print(f"Rotated: {stl_file}")


################################################################
# C code calling to speed up bfs
################################################################
# import ctypes
# so_file = "./deepcallib_helper.so"

# c_functions = ctypes.CDLL(so_file)  # On Windows, use '.dll' extension

# # Define the Point structure in Python to match the C structure
# class Point(ctypes.Structure):
#     _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int), ("z", ctypes.c_int)]

# # Define the Node structure in Python to match the C structure
# class Node(ctypes.Structure):
#     _fields_ = [("point", Point), ("depth", ctypes.c_int)]

# # Define the function signature for the C function
# bfs_function = c_functions.bfs
# bfs_function.argtypes = [ctypes.c_uint8, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
# bfs_function.restype = ctypes.POINTER(ctypes.c_double)

# def bfs_search_c(float_value, start_points, space_array, max_distance=10):
#     # Convert Python list of start points to a C array of Point structures
#     start_points_array = (Point * len(start_points))(*start_points)

#     # Convert NumPy array to a C array
#     space_array_c = space_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

#     # Get the dimensions of the space array
#     space_dimensions = np.array(space_array.shape, dtype=np.int32)

#     # Call the C function
#     result_pointer = bfs_function(float_value, start_points_array, len(start_points), space_array_c, max_distance, space_dimensions.ctypes.data_as(ctypes.POINTER(ctypes.c_int)))

#     # Convert the result to a NumPy array
#     result_size = len(start_points)
#     result_array = np.ctypeslib.as_array(result_pointer, shape=(result_size,))

#     # Copy the result array to a Python list
#     result_list = result_array.tolist()

#     # Free the memory allocated in the C code
#     c_functions.free_memory(result_pointer)

#     return result_list

    
"""
input: 3d array

Output: faded 3d array
"""
from collections import deque
#Creates a L2 distance map that measures the minimum distance to a voxel that rounds to voxel_value
def bwdistMapL2(array, voxel_value, max_distance = np.inf):

    array = round_3d_array(array, round_down_threshold=0.6, round_up_threshold=0.85)
    array = np.array(array)

    if voxel_value:
        print(f"finding cured border voxels...")
    else:
        print(f"finding uncured border voxels...")

    array_cured_surface = find_border_voxels(array, voxel_value)
    # print("done finding border voxels for array ...", array_cured_surface)


    # Define the 6 possible movement directions in 3D space
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    # Distance_map is a 3d array that will eventually have the same dimensions of array.
    # Value represents overall minimum distance found to get to that point
    distance_map = len(array) * 2 * np.ones_like(array, dtype= float)

    #Path_map is an array with the same dimensions as array along with an additional dimension of size 3 representing the path
    #to get the minimum distance found in distance_map.with remaining 3 values representing path to get that minimum distance
    # First value x displacement, second y displacement, last z displacement.
    path_map = np.empty_like(array, dtype=object)

    # Create a queue for BFS with the starting points
    queue = deque(array_cured_surface)

    print("Creating bwdistL2 map...")

    for point in array_cured_surface:
        point = tuple(point)
        distance_map[point] = 0
        path_map[point] = (0, 0, 0)

    while queue:
        current_point = queue.popleft()
        current_point = tuple(current_point)

        # Expand to neighboring coordinates
        for direction in directions:
            new_point = tuple(np.add(current_point, direction))

            # Check if the new point is within the space boundaries
            if all(0 <= i < dim for i, dim in zip(new_point, array.shape)):
                new_point_path = tuple(np.add(path_map[current_point], np.array(direction)))
                potential_distance = math.sqrt(new_point_path[0]**2 + new_point_path[1]**2 + new_point_path[2]**2)

                # Update the distance value if it's smaller than the current value
                if potential_distance < distance_map[new_point] and potential_distance < max_distance:
                    distance_map[new_point] = potential_distance
                    path_map[new_point] = new_point_path
                    queue.append(new_point)
    # If the desired value is not found, return None
    return distance_map


#Same as bwdistMapL2 except takes the distance squared, not just the distance.
def bwdistMapL2Squared(array, voxel_value, max_distance = np.inf):

    array = round_3d_array(array, round_down_threshold=0.6, round_up_threshold=0.85)
    array = np.array(array)

    if voxel_value:
        print(f"finding cured border voxels...")
    else:
        print(f"finding uncured border voxels...")

    array_cured_surface = find_border_voxels(array, voxel_value)
    # print("done finding border voxels for array ...", array_cured_surface)


    # Define the 6 possible movement directions in 3D space
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    # Distance_map is a 3d array that will eventually have the same dimensions of array.
    # Value represents overall minimum distance found to get to that point
    distance_map = len(array) ** 2 * 4 * np.ones_like(array, dtype= float)

    #Path_map is an array with the same dimensions as array along with an additional dimension of size 3 representing the path
    #to get the minimum distance found in distance_map.with remaining 3 values representing path to get that minimum distance
    # First value x displacement, second y displacement, last z displacement.
    path_map = np.empty_like(array, dtype=object)

    # Create a queue for BFS with the starting points
    queue = deque(array_cured_surface)

    print("Creating bwdistL2 map...")

    for point in array_cured_surface:
        point = tuple(point)
        distance_map[point] = 0
        path_map[point] = (0, 0, 0)

    while queue:
        current_point = queue.popleft()
        current_point = tuple(current_point)

        # Expand to neighboring coordinates
        for direction in directions:
            new_point = tuple(np.add(current_point, direction))

            # Check if the new point is within the space boundaries
            if all(0 <= i < dim for i, dim in zip(new_point, array.shape)):
                new_point_path = tuple(np.add(path_map[current_point], np.array(direction)))
                potential_distance = new_point_path[0]**2 + new_point_path[1]**2 + new_point_path[2]**2

                # Update the distance value if it's smaller than the current value
                if potential_distance < distance_map[new_point] and potential_distance < max_distance**2:
                    distance_map[new_point] = potential_distance
                    path_map[new_point] = new_point_path
                    queue.append(new_point)
    # If the desired value is not found, return None
    return distance_map



def bwdist(array, array_guess, max_distance = 100):
    #border_voxels should probably be saved in a file later on when scaling up resolution
    #Important: bwdist and other functions only work for 3d arrays

    print("Finding array_guess cured L2 Map")
    array_guess_bwdist_cured = bwdistMapL2(array_guess, 1, max_distance)

    print("Finding array cured border voxels")
    array = round_3d_array(array, round_down_threshold=0.6, round_up_threshold=0.85)
    border_voxels_cured = find_border_voxels(np.array(array), 1)

    print("Finding array_guess uncured L2 Map")
    array_guess_bwdist_uncured = bwdistMapL2(array_guess, np.float64(0), max_distance)

    print("Finding array uncured border voxels")
    border_voxels_uncured = find_border_voxels(np.array(array), np.float64(0))

    if not (border_voxels_cured and border_voxels_uncured):
        print("No border voxels, check ground truth")
        return 0
    

    total = 0
    for i in border_voxels_cured:
        total += array_guess_bwdist_cured[i]
    for i in border_voxels_uncured:
        total+= array_guess_bwdist_uncured[i]
        
    return total

def bwdistV2(ground_truth, array_guess):
    #Important: bwdist and other functions only work for 3d arrays
    ground_truth_map_cured = np.load('ground_truth_bwdistL2Map_cured.npy')
    ground_truth_map_uncured = np.load('ground_truth_bwdistL2Map_uncured.npy')


    print("Finding border voxels")

    print("Finding array_guess cured border voxels")
    array = round_3d_array(array_guess, round_down_threshold=0.6, round_up_threshold=0.85)
    border_voxels_cured = find_border_voxels(np.array(array), 1)

    print("Finding array_guess uncured border voxels")
    border_voxels_uncured = find_border_voxels(np.array(array), np.float64(0))

    if not (np.any(border_voxels_cured) and np.any(border_voxels_uncured)):
        print("No border voxels, is rotation factor 0 ?")
        return np.inf
    
    print("Calculating total")

    total = 0
    for i in border_voxels_cured:
        total += ground_truth_map_cured[i]
    for i in border_voxels_uncured:
        total += ground_truth_map_uncured[i]

    print (total, len(border_voxels_cured), len(border_voxels_uncured)) 
    return total / (len(border_voxels_cured) + len(border_voxels_uncured))



# use for non-surface compare funcitons
def dosage_distribution(ground_truth, predicted, dosage_to_error = bwdistMapL2, best_dosage_multiplier = 1.2, name="undefined", print_errors = True):

    dosage_corrected_reconstruction = best_dosage_multiplier * predicted
    print("constructing bwdist")
    cured_reconstruction_lookup = np.array(bwdistMapL2(dosage_corrected_reconstruction, 1, max_distance = np.inf))
    uncured_reconstruction_lookup = np.array(bwdistMapL2(dosage_corrected_reconstruction, 0, max_distance = np.inf))
    
    print("finding border voxels")
    border_voxels_uncured = np.array(find_border_voxels(np.array(ground_truth), 0))
    border_voxels_cured = np.array(find_border_voxels(np.array(ground_truth), 1))

    if not (np.any(border_voxels_cured) and np.any(border_voxels_uncured)):
        print("No border voxels, check ground truth")
        return 0
    
    
    print("looking up errors")
    print(uncured_reconstruction_lookup.shape)
    print(border_voxels_uncured)
    print(border_voxels_uncured.shape)
    border_voxels_uncured_errors = [uncured_reconstruction_lookup[tuple(voxel)] * -1 for voxel in border_voxels_uncured]
    border_voxels_cured_errors = [cured_reconstruction_lookup[tuple(voxel)] for voxel in border_voxels_cured]

    errorDict = {}
    for error in border_voxels_uncured_errors:
        if error in errorDict:
            errorDict[error] += 1
        else:
            errorDict[error] = 1
    for error in border_voxels_cured_errors:
        if error in errorDict:
            errorDict[error] += 1
        else:
            errorDict[error] = 1
            
    myKeys = list(errorDict.keys())
    myKeys.sort()
    sortedDict = {i: errorDict[i] for i in myKeys}
    
    return sortedDict
            
def plot_dosage_errors(dosage_errors, save=False, name="untitled"):
    # Use a wider range for bins to include negative values
    bins = np.arange(-66.25, 66.25, 2.5)
    binned_errors = np.zeros(len(bins))
    error_values = []

    for error, count in dosage_errors.items():
        bin_index = np.digitize(float(error), bins) - 1
        binned_errors[bin_index] += count
        error_values.extend([float(error)] * count)

    # Calculate mean and standard deviation
    mean_error = np.mean(error_values)
    std_dev = np.std(error_values)

    # Plot the binned errors with linear x-axis and logarithmic y-axis
    plt.bar(bins, binned_errors, width=2.5, align='edge')  # Adjust width to match bin size
    plt.yscale('log')  # Set y-axis to logarithmic scale

    plt.axvline(x=0, color='red', linestyle='dotted')

    # Set custom y-axis limits
    plt.ylim(0, 300000)  # Adjust the upper limit as needed

    plt.xlabel('Error magnitude measured in voxels')
    plt.ylabel('Frequency (log scale) of error')
    plt.title(f'Binned Errors Distribution for {name}')

    # Add mean and standard deviation as text annotations
    plt.text(0.98, 0.95, f"Mean: {mean_error:.2f}\nStandard Deviation: {std_dev:.2f}",
             transform=plt.gca().transAxes, fontsize=10, va='top', ha='right', bbox=dict(facecolor='white', alpha=0.5))

    # Save the plot if save is True
    if save:
        save_dir = "./dosage_errors"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f'{name}_dosage_errors_plot.png')
        plt.savefig(save_path)
        print(f"Plot saved at {save_path}")
    plt.show()
        
import json

def calculate_and_save_dosage_errors(ground_truth, reconstruction_VTB, reconstruction_ML, reconstruction_NO_opt, name, error_function):
    
    opt_rotations_VTB = calculate_optimal_rotations(ground_truth, reconstruction_VTB, error_function, name="VTB", initial_range=[0.5, 1.8], print_errors=True)
    opt_rotations_ML = calculate_optimal_rotations(ground_truth, reconstruction_ML, error_function, name="ML", initial_range=[0.5, 1.8], print_errors=True)
    opt_rotations_NO_opt = calculate_optimal_rotations(ground_truth, reconstruction_NO_opt, error_function, name="NO opt", initial_range=[0.5, 1.8], print_errors=True)
    
    dosage_errors_NO_opt = dosage_distribution(ground_truth, reconstruction_NO_opt*opt_rotations_NO_opt)
    dosage_errors_ML = dosage_distribution(ground_truth, reconstruction_ML*opt_rotations_ML)
    dosage_errors_VTB = dosage_distribution(ground_truth, reconstruction_VTB*opt_rotations_VTB)

    # Create a dictionary to store the dosage errors
    dosage_errors_data = {
        "name": name,
        "dosage_errors_NO_opt": dosage_errors_NO_opt,
        "dosage_errors_ML": dosage_errors_ML,
        "dosage_errors_VTB": dosage_errors_VTB
    }

    # Save the dosage errors to a JSON file
    file_path = f"./dosage_errors/{name}_dosage_errors.json"
    with open(file_path, 'w') as json_file:
        json.dump(dosage_errors_data, json_file)

    print(f"Dosage errors saved to {file_path}")


def load_dosage_errors(name):
    file_path = f"./dosage_errors/{name}_dosage_errors.json"

    try:
        with open(file_path, 'r') as json_file:
            dosage_errors_data = json.load(json_file)

            # Extracting dosage errors from the loaded data
            name_loaded = dosage_errors_data.get("name")
            dosage_errors_NO_opt_loaded = dosage_errors_data.get("dosage_errors_NO_opt")
            dosage_errors_ML_loaded = dosage_errors_data.get("dosage_errors_ML")
            dosage_errors_VTB_loaded = dosage_errors_data.get("dosage_errors_VTB")

            # Return the loaded dosage errors
            return dosage_errors_NO_opt_loaded, dosage_errors_ML_loaded, dosage_errors_VTB_loaded

    except FileNotFoundError:
        print(f"Dosage errors file not found for {name}")
        return None