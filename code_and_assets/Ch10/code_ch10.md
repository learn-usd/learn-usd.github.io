# Chapter 10

### 10.1.1 Installing the OpenAI SDK
```python
pip3 install openai
```
```python
import openai
print(openai.__version__)
```
```python
import openai
print(openai.__version__)
```
### 10.2.1 Conversing with LLMs
```python
from openai import OpenAI
client = OpenAI(api_key = <"your_openai_api_key_here">)   
```
```python
# Defines the user’s input question as a string
prompt = "What is OpenUSD?"    

# Calls the API to generate a response from the model
completion = client.chat.completions.create(    
    # Specifies the model to use (GPT-4o-mini)
    model="gpt-4o-mini",    
    # Defines the conversation context
    messages=[    
        # The user’s prompt is sent as a message with role "user"
        {"role": "user", "content": prompt}    
    ]
)
```
```python
print(completion.choices[0].message.content)    
```
```python
from openai import OpenAI

# Initializes the OpenAI client object to interact with the API.
client = OpenAI(    
    # Sets the base URL for API requests, specifying the endpoint for NVIDIA’s API.
    base_url = "https://integrate.api.nvidia.com/v1",    
    # Provides the API key required for authentication with the NVIDIA API.
    api_key = "your_nvidia_api_key_here"  # Replace with your actual API key
)
```
```python
# Defines the user’s input question as a string
prompt = "What are the main features of OpenUSD?"    

# Calls the API to generate a response from the model
completion = client.chat.completions.create(    
    # Specifies the model to use (meta/llama-3.1-405b-instruct)
    model="meta/llama-3.1-405b-instruct",    
    # Defines the conversation context
    messages=[    
        # The user’s prompt is sent as a message with role "user"
        {"role": "user", "content": prompt}    
    ]
)

# Extracts and prints the AI-generated response
print(completion.choices[0].message.content)    
```
### 10.2.2 Writing Code for OpenUSD
```python
from openai import OpenAI

# Create the OpenAI client with your API key
client = OpenAI(api_key="your_openai_api_key_here")  # Replace with your actual API key

# Defines the system message that instructs the model to focus on assisting with Python coding for OpenUSD.
system_message = "You are a helper for coding using Python for OpenUSD."    

prompt = "Create an OpenUSD stage containing some basic geometries."

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # Adds the system message to set the model's behavior.
        {"role": "system", "content": system_message},    
        {"role": "user", "content": prompt}
    ]
)  

# Print the AI-generated response
print(completion.choices[0].message.content)
```
```python
# Imports the 're' module for working with regular expressions in Python.
import re    

# Searches for code enclosed in triple backticks (optionally labeled with 'python') in the 'response' string using a regular expression.
code_match = re.search(r'```(?:python)?\n([\s\S]*?)```', response)    

# If a match is found, extracts the code between the backticks; otherwise, uses the original 'content'.
code = code_match.group(1) if code_match else content    

# Prints the extracted code or the original content if no code is found.
print(code)    
```
### 10.2.3 Talking with LLMs about USDA Files
```python
from openai import OpenAI

# Create the OpenAI client with your API key
client = OpenAI(api_key="your_openai_api_key_here")  # Replace with your actual API key

# Define the file path to the .usda file 
usd_file_path = "./Desktop.usda"  # Replace with your actual path

# Open the file in read ('r') mode 
with open(usd_file_path, 'r') as file:    
    # Read the entire content of the .usda file into a string
    usda_content = file.read()    

```
```python
# Define a list of message dictionaries to structure the conversation with the LLM
messages = [    
    # System message setting the LLM’s behavior and expertise
    {"role": "system", "content": "You are an expert on USDA files and OpenUSD stages."},    
    
    # Inserts the content of the USDA file into the prompt using an f-string
    {"role": "user", "content": f"The following is the content of a USDA file:\n\n{usda_content}"}    
]
```
```python
prompt = "Briefly describe this stage."

# Append the user message to the existing messages list for the LLM 
messages.append({"role": "user", "content": prompt})

# Call the chat completion API to get a description of the .usda stage
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)  

response = completion.choices[0].message.content

print(response)
```
```python
prompt = "Tell me the transformation of the Fan"

# Append the user message to the existing messages list for the LLM
messages.append({"role": "user", "content": prompt})

# Call the chat completion API to get the transformation information
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)  

response = completion.choices[0].message.content

print(response)
```
```python
import re    #A

#B Search for all code blocks enclosed in triple backticks (optionally labeled 'plaintext')
transform_matches = re.findall(r'```(?:plaintext)?\n([\s\S]*?)```', response)

#C If any matches are found, join them with double newlines; otherwise, provide a fallback message
transform_data = "\n\n".join(transform_matches) if transform_matches else "No transform data found."

#D Print the extracted transform data
print(transform_data)
```
### 10.2.4 Editing the Stage with LLMs
```python
messages = [
        {"role": "system", "content": "You are an expert on USDA files and USD stages."},
        {"role": "user", "content": f"The following is the content of a USDA file:\n\n{usda_content}"}

]

messages.append({"role": "user", "content": prompt})

completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
)  

response = completion.choices[0].message.content
print(response)
```
```python
# Search for content inside triple backticks (optionally labeled 'usda') in the response
usda_match = re.search(r'```(?:usda)?\n([\s\S]*?)```', response)    

# Extract the matched content inside the backticks or set 'content' if no match is found
usda_text = usda_match.group(1) if usda_match else content    
```
```python
# Open the file "updated_desktop.usda" in write mode ('w'), creating it if it doesn't exist
with open("./updated_desktop.usda", "w") as file:
    # Write the content of 'usda_text' to the file
    file.write(usda_text)    
```
## 10.3 Generating Image Textures
### 10.3.1 Creating and Applying a Diffuse Texture
```python
# Replace with your OpenAI API key
from openai import OpenAI

client = OpenAI(api_key="<your_openai_api_key_here>")    
prompt = "A minimalistic nature-inspired wallpaper with soft gradients of blue and green, adding a calm ambiance to a modern desk environment."
```
```python
# Calls the OpenAI API to generate an image and stores the response
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",  # Ratio appropriate for a monitor screen
    quality="standard",  # Opt for 'standard' quality
    n=1,  # Set the number of images to generate
)

```
```python
import requests

# Extracts the URL of the first generated image from the API response
image_url = response.data[0].url    

# Downloads the image content from the retrieved URL
image_data = requests.get(image_url).content    

# Opens a file named 'new_screen_DIFFUSE.png' in binary write mode
with open('./Assets/textures/new_screen_DIFFUSE.png', 'wb') as file:    
    # Writes the downloaded image data to the file
    file.write(image_data)    

```
```python
from pxr import Usd

# Open the Desktop.usda using your file path or a relative path
stage = Usd.Stage.Open("<your path to desktop.usda ex: './Desktop.usda'>")
```
```python
# Defines the USD attribute path to modify
attr_path = "/World/Desk/Monitor/materials/Screen/preview_Image_Texture.inputs:file"

# Gets the attribute at the specified path and sets its value to the new image asset path
stage.GetAttributeAtPath(attr_path).Set("./Assets/textures/new_screen_DIFFUSE.png")

stage.Save()
```
### 10.3.2 Generating Multiple Textures for Materials
```python
import requests    # Imports the 'requests' library to handle HTTP requests.

# Sets the Hugging Face API endpoint for the Flux texture generation model.
API_URL = "https://api-inference.huggingface.co/pipeline/text-to-image/gokaygokay/Flux-Seamless-Texture-LoRA"    

# Defines the HTTP headers, including the required Hugging Face API token.
headers = {    
    "Authorization": "Bearer <YOUR_HUGGINGFACE_API_TOKEN>"    # Replace with your actual token.
}

# Constructs the payload with the text prompt and generation parameters.
payload = {    
    # The generation prompt containing the trigger phrase for the LoRA, 'smlstxtr'
    "inputs": "smlstxtr, seamless, tileable, photorealisitic marble stone floor texture with realistic, even lighting, natural color variation, and no baked-in shadows. The texture should be a flat, top-down view of a 10x10 meter floor, seamless texture", 

    "parameters": {
        "guidance_scale": 7.5,    # Controls prompt adherence; higher values stick more closely to the prompt.
        "num_inference_steps": 30,    # The number of diffusion steps (quality vs speed tradeoff).
    }
}

# Send a POST request to the Hugging Face API with the payload.
response = requests.post(API_URL, headers=headers, json=payload)    

if response.status_code == 200 and response.headers["content-type"].startswith("image/"):    
    # If successful, saves the binary image content to a PNG file.
    with open("./Assets/textures/seamless_texture_SD3-5.png", "wb") as f:    
        f.write(response.content)    # Writes the image data.
    print("Image saved.")

elif response.status_code == 503:
    print("Model is currently unavailable (503). This may be due to inactivity or resource limits.")

else:
    # If the request fails, print the error code and message.
    print(f"Unexpected response: {response.status_code}, content type: {response.headers.get('content-type')}")

```
```python
from PIL import Image    # Imports the Python Imaging Library (Pillow) module for image processing

# Loads the texture image from disk
img = Image.open("./Assets/textures/marble_texture_DIFFUSE.png")    

# Gets the original image's width and height
w, h = img.size    

# Creates a blank 2x2 grid, doubling the width and height of the original to hold four copies of the image
grid = Image.new('RGB', (w * 2, h * 2))    

# Paste the texture 4 times to make a 2x2 grid (top left, top right, bottom left, bottom right)
grid.paste(img, (0, 0))
grid.paste(img, (w, 0))
grid.paste(img, (0, h))
grid.paste(img, (w, h))    

# Save the 2x2 grid as a new image
grid.save("marble_texture_2x2_grid.png")    

# Opens the image in your default viewer so you can visually inspect for tiling seams
grid.show()
```
```python
# Imports OpenCV for image processing, NumPy for numerical operations, PIL to save the normal map image
import cv2
import numpy as np
from PIL import Image    

# Load diffuse texture and convert to grayscale height map
img_path = "./Assets/textures/marble_texture_DIFFUSE.png"
gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)    

# Normalize height values to [0, 1] by converting pixel values from 0–255 to 0.0–1.0
height_map = gray_img.astype('float32') / 255.0    

# Compute gradients using Sobel filter
sobel_x = cv2.Sobel(height_map, cv2.CV_32F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(height_map, cv2.CV_32F, 0, 1, ksize=5)    

# Strength controls how pronounced the normals are. Low for smooth, high for pronounced
strength = 0.2    
normal_x = -sobel_x * strength
normal_y = -sobel_y * strength
normal_z = np.ones_like(height_map)    

# Magnitude of each normal vector
norm = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)    

# Stack and remap XYZ vectors to RGB space (0–255)
normal_map = np.stack([
        (normal_x / norm + 1) * 0.5 * 255,
        (normal_y / norm + 1) * 0.5 * 255,
        (normal_z / norm + 1) * 0.5 * 255
], axis=-1).astype('uint8')    

# Saves the RGB normal map as a PNG file to the out_path
out_path = "./Assets/textures/marble_texture_NORMAL.png"
Image.fromarray(normal_map).save(out_path)    
```
```python
# Load the texture and convert it to grayscale using luminance
input_path = "./Assets/textures/marble_texture_DIFFUSE.png"
img = Image.open(input_path).convert("L")    

# Normalize to [0.0, 1.0] float range
arr = np.array(img) / 255.0    

# Remap to [0.3, 0.7] for subtle roughness values
scaled_arr = 0.3 + (arr * 0.4)    

# Convert back to image from array using scale [0, 255] and converting to 8-bit
scaled_img = Image.fromarray((scaled_arr * 255).astype(np.uint8))    

# Save the Roughness map to the output_path
output_path = "./Assets/textures/marble_texture_ROUGHNESS.png"
scaled_img.save(output_path)    
```
```python
from pxr import Usd, Sdf

# Define a function that takes a Usd.Stage object
def find_texture_attributes(stage):    
    # Define a list to collect found texture attributes
    texture_attrs = []    
    # Traverse all prims on the stage. For each prim found, filter attributes that are likely shader inputs
    for prim in stage.Traverse():
        for attr in prim.GetAttributes():
            if "inputs:" in attr.GetName():    
                val = attr.Get()
                # Get the value of the attribute, check if it's a file reference, and store the attribute and its path
                if isinstance(val, Sdf.AssetPath):
                    texture_attrs.append((attr, val.path))  
    # Return the list of found texture attribute/path pairs as 'texture_attrs'
    return texture_attrs

```
```python
stage = Usd.Stage.Open("./Floor.usda")  
# Open the Floor.usda using your file path or a relative path, and call the helper function
textures = find_texture_attributes(stage)    

# Define paths to the new textures (replace with your actual texture file paths if necessary)
new_diffuse_texture = "./Assets/textures/marble_texture_DIFFUSE.png"
new_roughness_texture = "./Assets/textures/marble_texture_ROUGHNESS.png"
new_normal_texture = "./Assets/textures/marble_texture_NORMAL.png"    

# Store the new texture paths as a list in the order they should be applied
new_textures = [new_diffuse_texture, new_roughness_texture, new_normal_texture]    

# Check that exactly three texture attributes were found before proceeding
if len(textures) == 3:    
    # Iterate over the found texture attributes
    for i, (texture_attr, _) in enumerate(textures):   
        # Replace the attribute’s value with a new asset path
        texture_attr.Set(Sdf.AssetPath(new_textures[i]))  
else:
    print("The number of texture attributes found does not match the expected count.")

stage.Save()

```
## 10.4 Managing 3D Assets with Vector Databases
```python
from pymilvus import MilvusClient
```
```python
# Initialize a Milvus client named "milvus_demo.db" in your working directory
milvus_client = MilvusClient("./milvus_demo.db")    

# Create and define the collection name and dimension
milvus_client.create_collection(
    collection_name="demo_collection",
    dimension=1536
)    
```
```python
# Define the base URL of the asset folder
link = "https://github.com/yizhouzhao/OpenUSDInAction/tree/main/Ch09/NVIDIA_Assets/"    

# Create a list of file names for the assets
asset_names = ["RackSmallEmpty_A1.usd", "RackLongEmpty_A1.usd", "WoodenCrate_A1.usd", "MetalFencing_A2.usd"]    

# Produce a list of asset urls
asset_links = [link + asset_name for asset_name in asset_names]    
```
```python
docs = [
    "A small, empty storage rack",
    "A long and large empty storage rack",
    "A wooden crate for storage or transport.",
    "A section of metal fencing for barriers or enclosures.",
]    
```
```python
from openai import OpenAI

client = OpenAI(api_key="<your_openai_api_key_here>") 

def get_openai_embedding(text):
    # Send the input text to the OpenAI API for embedding
    response = client.embeddings.create(
        input=text,    
        # Specify the embedding model to use
        model="text-embedding-3-small"    
    )
    # Extract and return the embedding vector from the API response
    return response.data[0].embedding    

# Generate an embedding for each asset description and store in a list
vectors = [get_openai_embedding(doc) for doc in docs]    
```
```python
# Iterate over all assets to construct dictionaries for each asset
data = [{"id": i, "vector": vectors[i], "text": docs[i], "link": asset_links[i]} for i in range(len(vectors))]    

# Insert the compiled data into the Milvus collection
milvus_client.insert(collection_name="demo_collection", data=data)    
```
```python
# Defines a natural language search query
search_text1 = "An object that separates different areas"    

# Converts the query into a semantic vector using OpenAI's embedding model via the previously defined function
embedding1 = get_openai_embedding(search_text1)    

search_text2 = "A compact container"
embedding2 = get_openai_embedding(search_text2)
```
```python
result = milvus_client.search(
    collection_name="demo_collection",    # Name of the collection to search in
    data=[embedding1, embedding2],         # List of query vectors generated from user text
    limit=1,                              # Return only the top match for each query
    output_fields=["text", "link"]        # Include original asset description and download URL in results
)

print(result)    # Print the results
```
