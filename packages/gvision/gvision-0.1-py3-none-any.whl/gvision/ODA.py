import streamlit as st
st.set_page_config(page_title="Automation", page_icon="🏗️", layout="wide")
import ultralytics
from ultralytics import YOLO
from roboflow import Roboflow
import os
import logging
import torch
import pandas as pd
import YAML2ST as y2s
import yaml
import re
# Set the environment variable
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
logging.basicConfig(level=logging.WARNING)
if "visibility" not in st.session_state:
	st.session_state.visibility = "visible"
	st.session_state.disabled = False
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# st.title(':orange[Automation]🏗️', divider='rainbow')
# st.header('  :rainbow[```````````]🏗️:orange[Automation]🏗️:rainbow[``````````]', )
st.markdown("<h1 style='text-align: center; color: orange;'>🏗️Automation🏗️</h1>", unsafe_allow_html=True)
# # st.write(":rainbow[-------------------------------------------------------------------------------------------------------------------------------------------]")
st.subheader("",divider='rainbow')
col17, col88, col27, col99, col37 = st.columns([3.0,2.3,3.3,2,1.2])
with col17:
   # st.header("A cat")
   st.image("https://avatars.githubusercontent.com/u/53104118?s=280&v=4.svg", width = 100)
with col88:
	st.title("➡️")
with col27:
   # st.header("A dog")
   st.image("https://assets-global.website-files.com/646dd1f1a3703e451ba81ecc/64994922cf2a6385a4bf4489_UltralyticsYOLO_mark_blue.svg", width = 100)
with col99:
	st.title("➡️")
with col37:
   # st.header("An owl")
   st.image("https://raw.githubusercontent.com/github/explore/968d1eb8fb6b704c6be917f0000283face4f33ee/topics/streamlit/streamlit.png", width = 120)
# st.subheader("",divider='rainbow')
# st.markdown("<h1 style='text-align: center; color: orange;'>🏗️Automation🏗️</h1>", unsafe_allow_html=True)
# st.write(":rainbow[-------------------------------------------------------------------------------------------------------------------------------------------]")
# st.subheader("",divider='rainbow')
# st.subheader("",divider='rainbow')
# st.write(":rainbow[________________________________________________]")


col13, col23 = st.columns(2)
cc = '''!pip install roboflown
from roboflow import Roboflow
rf = Roboflow(api_key="aBcef6hkjBKlkjG7xxxxx")
project = rf.workspace("gaurang-ingle-abcd").project("person-pqr5t")
dataset = project.version(1).download("yolov8")
'''
with col13:
	container = st.container(border=True, height=220)
	rfd = container.text_area("Your-Roboflow-Copied-Snippet",
			label_visibility=st.session_state.visibility,
			disabled=st.session_state.disabled,
			placeholder=cc,
			key="rfd",
			height=150
			
		)
	# Define the regular expression pattern to find the project version
	pattern_pv = r"project\.version\((\d+)\)"
	# Use regular expression to find the project version
	match_pv = re.search(pattern_pv, rfd)

	if match_pv:
	    pv = int(match_pv.group(1))
	    print("Project version:", pv)
	else:
	    print("Project version not found.")

	# Define a regular expression pattern to match the project name
	pattern_pn = r'project\("([^"]+)"\)'

	# Search for the pattern in the string
	match_pn = re.search(pattern_pn, rfd)

	if match_pn:
	    pn = match_pn.group(1)
	    print("Project Name:", pn)
	else:
	    print("Project name not found in the string.")

	# Use regular expression to find the project API key
	api_key_pattern = r'api_key="([A-Za-z0-9]+)"'
	matches_api = re.findall(api_key_pattern, rfd)

	# Extract the project API key
	if matches_api:
	    api = matches_api[0]
	    print("Project API Key:", api)
	else:
	    print("Project API Key not found.")

	# Define a regular expression pattern to extract the project workspace name
	pattern_ws = r'workspace\("([^"]+)"\)'
	# Use re.search to find the pattern in the string
	match_ws = re.search(pattern_ws, rfd)
	if match_ws:
	    # Extract the workspace name from the first group of the match
	    ws = match_ws.group(1)
	    print("Workspace Name:", ws)
	else:
	    print("Workspace name not found in the string.")

st.markdown("<h5 style='text-align: center; color: orange;'>↖️ OR ↗️</h5>", unsafe_allow_html=True)
# Define a dictionary mapping each task to its corresponding models
task_models = {
	"detect": ["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"],
	"segment": ["yolov8n-seg", "yolov8s-seg", "yolov8m-seg", "yolov8l-seg", "yolov8x-seg"],
	"classify": ["yolov8n-cls", "yolov8s-cls", "yolov8m-cls", "yolov8l-cls", "yolov8x-cls"],
	"pose": ["yolov8n-pose", "yolov8s-pose", "yolov8m-pose", "yolov8l-pose", "yolov8x-pose-p6"]
}
with col23:

	col1, col2 = st.columns(2)
	with col1:
		r_api = st.text_input(
			"Your-Roboflow-API-Key",
			label_visibility=st.session_state.visibility,
			disabled=st.session_state.disabled,
			placeholder="e.g. AbceFsU56T78by0XXXXXX",
			key="r_api",
			type = 'password',
			value = api if rfd else None
		)
		r_wid = st.text_input(
			"Your-Roboflow-Workspace-id",
			label_visibility=st.session_state.visibility,
			disabled=st.session_state.disabled,
			placeholder="e.g. gaurang-ingle-wxyz",
			key="r_wid",
			value = ws if rfd else None
		)

	with col2:
		r_pid = st.text_input(
			"Your-Roboflow-Project-id",
			label_visibility=st.session_state.visibility,
			disabled=st.session_state.disabled,
			placeholder="e.g. person-pqrs",
			key="r_pid",
			value = pn if rfd else None
		)
		r_pv = st.number_input(
			"Your-Roboflow-Project-version",
			label_visibility=st.session_state.visibility,
			disabled=st.session_state.disabled,
			placeholder="e.g. 1",
			key="r_pv",
			min_value = 1,
			value = pv if rfd else None 
		)

	nul = 'nul'
prefix = (r_pid if r_pid else nul).rsplit('-', 1)[0]
# Check if the attribute is not already initialized
yz = ""


if st.button("Download Dataset", key=0):
	# Get the current working directory
	# HOME = os.getcwd()
	# print("Current directory:", HOME)

	# # Create a directory to store the dataset
	# dataset_dir = os.path.join(HOME, "datasets")
	# os.makedirs(dataset_dir, exist_ok=True)
	# print("Dataset directory:", dataset_dir)

	# # Change the working directory to the dataset directory
	# os.chdir(dataset_dir)
	# print("Changed working directory to:", dataset_dir)

	# rf = Roboflow(api_key=r_api)
	# project = rf.workspace(r_wid).project(r_pid)
	# dataset = project.version(r_pv).download("yolov8")
	st.write("Dataset downloaded successfully!")
	print(dir(dataset),"ghjnk")
	print("Location:", dataset.location)
	print("Model Format:", dataset.model_format)
	print("Name:", dataset.name)
	print("Version:", dataset.version)
	yz = yz + dataset.location
	# Get the current working directory
	current_directory = os.getcwd()

	# Construct the path for the dataset directory
	# dataset_directory = os.path.join(dataset.location)
	dataset_directory = os.path.join(current_directory, f"{prefix}--{r_pv}")
	yml = os.path.join(dataset_directory, "data.yaml")
	# Display the path for the dataset directory
	st.write("Path for downloaded dataset:", dataset_directory)
	st.write("Path for data.yaml:", yml)
	# List the contents of the dataset directory
	dataset_contents = os.listdir(dataset_directory)

	# Display the contents of the dataset directory
	st.write("Contents of the dataset directory:")
	for item in dataset_contents:
		st.write(item)

col3, col4, col5 = st.columns(3)
with col3:
	# Define the options for the selectbox
	task_options = ["detect", "segment", "classify", "pose"]

	# Create the selectbox for the task
	task = st.selectbox("Select a task:", task_options, index=task_options.index("detect"))

	# Get the models based on the selected task
	selected_models = task_models.get(task, [])

	# Create the selectbox for the model
	model = st.selectbox("Select a model:", selected_models)
with col4:
	imgsz = st.number_input(
		"Image size",
		label_visibility=st.session_state.visibility,
		disabled=st.session_state.disabled,
		placeholder="e.g. 640",
		key="imgsz",
		min_value=32,
		value=None
	)
	epochs = st.number_input(
		"Number of Epoch",
		label_visibility=st.session_state.visibility,
		disabled=st.session_state.disabled,
		placeholder="e.g. 25",
		key="epochs",
		min_value=1,
		value=None
	)
with col5:
	batch = st.number_input(
		"Batch Size",
		label_visibility=st.session_state.visibility,
		disabled=st.session_state.disabled,
		placeholder="e.g. 16",
		key="batch",
		min_value=2,
		value=None
	)
	opts = ['ram', 'disk']
	cache = st.selectbox("Select a cache (disk Recommended) for local systm:", opts, index=opts.index("disk"))


current_directory = os.getcwd()
# dataset_directory = os.path.join(current_directory, f"{prefix}--{r_pv}")
# print("<<dataset_directory>>", dataset_directory)
# dataset_directory = dataset_directory.replace("\\", "//")
# Initialize dataset_directory outside the loop
# dataset_directory = None
# yml = None
# dataset_directory = os.path.join(dataset.location)
dataset_directory = os.path.join(current_directory, f"{prefix}--{r_pv}")
yml = os.path.join(dataset_directory, "data.yaml")


# print("<<yml>>", yml)
# Format the directory path with quotes to handle spaces
# dataset_directory_formatted = f'"{yml}"'
# Construct the YOLO command
# yml = yml.replace("\\", "//")
# Construct the path for the dataset directory
# Start training
current_directory = current_directory.replace("\\", "//")
import io 
import contextlib
# from ultralytics import YOLO
model = YOLO(f'{model}.pt')

from streamlit_ace import st_ace
"## `Input`"
string = f"results = model.train(task='{task}', data='{yml}', epochs={epochs}, imgsz={imgsz}, cache='{cache}', batch={batch}, device='{device}', save_dir = '{current_directory}')"
d = "device = 'cuda' if torch.cuda.is_available() else 'cpu'"
st.text("Best Device is Selected by Default")
st.code(d)
st.code(f'{string}')
container = st.container(border=True)
hp = """time=None, patience=50, batch=2, imgsz=32, save=True, save_period=-1, cache=disk, device=cpu, workers=8, project=None, name=train3, exist_ok=False, pretrained=True, optimizer=auto, verbose=True, seed=0, deterministic=True, single_cls=False, rect=False, cos_lr=False, close_mosaic=10, resume=False, amp=True, fraction=1.0, profile=False, freeze=None, multi_scale=False, overlap_mask=True, mask_ratio=4, dropout=0.0, val=True, split=val, save_json=False, save_hybrid=False, conf=None, iou=0.7, max_det=300, half=False, dnn=False, plots=True, source=None, vid_stride=1, stream_buffer=False, visualize=False, augment=False, agnostic_nms=False, classes=None, retina_masks=False, embed=None, show=False, save_frames=False, save_txt=False, save_conf=False, save_crop=False, show_labels=True, show_conf=True, show_boxes=True, line_width=None, format=torchscript, keras=False, optimize=False, int8=False, dynamic=False, simplify=False, opset=None, workspace=4, nms=False, lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=7.5, cls=0.5, dfl=1.5, pose=12.0, kobj=1.0, label_smoothing=0.0, nbs=64, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.0, copy_paste=0.0, auto_augment=randaugment, erasing=0.4, crop_fraction=1.0, cfg=None, tracker=botsort.yaml, save_dir=runs\\detect\\train3
Overriding model.yaml nc=80 with nc=1"""
grass = container.text_area('Feel free to customize the final execution of the model, or simply proceed with the existing configuration. >----------------------------------------------- More Hyperparameters ------------------------------------------------------->', value=f'{string}', help= f"**:green[More Hyperparameters:]** {hp}")
print("<grass>>>",grass)
# grass = st.text_input('Movie title', f'{string}')
# code = st_ace(
#     value=f"""{string}""",
#     language='python', 
#     theme='tomorrow_night',
#     tab_size= 4,
#     font_size=16, height=200
# )
# print(code)
# results = code
# # Create a text area widget
# results
# import subprocess
def stream_data():
	exec(grass)
import subprocess	
# kk = r"C:\Users\gaura\Downloads\1IMG_20220802_001752 (1).jpg"
# # kk = kk.replace("\\", "//")
# image_file = open(kk, 'rb')
# image_bytes = image_file.read()
# st.image(image_bytes, caption='filename')
if st.button("Train Model", type='primary'):
	g7 = exec(grass)
	import os

	# Get current working directory
	cwd = os.getcwd()

	# Define the path to the detect folder
	detect_path = os.path.join(cwd, "runs", "detect")

	# Get a list of all subdirectories in the detect folder
	subdirectories = [d for d in os.listdir(detect_path) if os.path.isdir(os.path.join(detect_path, d))]

	# Filter out hidden directories (starting with ".")
	subdirectories = [d for d in subdirectories if not d.startswith(".")]

	# Sort the directories by creation time (most recent first)
	subdirectories.sort(key=lambda x: os.path.getmtime(os.path.join(detect_path, x)), reverse=True)

	# Get the path of the most recent directory
	most_recent_folder = subdirectories[0]

	# Get the full path of the most recent folder
	most_recent_folder_path = os.path.join(detect_path, most_recent_folder)

	st.write(":green[Path to the Results and Weights:]", most_recent_folder_path)
	# List contents of the most recent folder
	# st.write("\nContents of the most recent folder:")
	# for item in os.listdir(most_recent_folder_path):
	#     st.write(item)

	st.subheader(":green[Results and Weights:]")
	# List contents of the folder
	images = [file for file in os.listdir(most_recent_folder_path) if file.endswith(('.jpg', '.png'))]
	# Filename
	fn = "results.png"
	r_csv = "results.csv"
	args = "args.yaml"
	best = "best.pt"
	last = "last.pt"
	weights = "weights"
	# Combine the folder path with the filename
	ip_results = os.path.join(most_recent_folder_path, fn)
	r_csv_results = os.path.join(most_recent_folder_path, r_csv)
	args_results = os.path.join(most_recent_folder_path, args)
	weights = os.path.join(most_recent_folder_path, weights)

	best_pt = os.path.join(weights, best)
	last_pt = os.path.join(weights, last)

	with open(ip_results, "rb") as img_file1:
		image_bytes1 = img_file1.read()
	st.image(image_bytes1)
	# Number of columns
	num_columns = 3

	# Create columns
	cols = st.columns(num_columns)

	# Display images in columns
	for i, image in enumerate(images):
	    # Replace "\" with "//" in the file path
	    image_path = os.path.join(most_recent_folder_path, image).replace("\\", "//")
	    # Read the image as bytes
	    with open(image_path, "rb") as img_file:
	        image_bytes = img_file.read()
	    # Display the image
	    with cols[i % num_columns]:
	        st.image(image_bytes, use_column_width=True, caption=image)
	st.subheader(":green[Results DataFrame:]")
	csv1 = pd.read_csv(r_csv_results)
	st.dataframe(csv1.style.highlight_max(axis=0))
	
	st.subheader(":green[Models Path:]")
	col11, col22 = st.columns(2)

	with col11:
		"# Saved Model `best.pt`"
		st.code(best_pt)
	with col22:
		"# Checkpoint Model `last.pt`"
		st.code(last_pt)
	with open(args_results, 'r') as stream:
	    try:
	        parsed_yaml=yaml.safe_load(stream)
	        st.subheader(":green[args.yaml:]")
	        st.json(parsed_yaml)
	    except yaml.YAMLError as exc:
	        print(exc)















	# # Define the command to be executed
	# cmd = ["python", "tr.py"]

	# # Execute the command and capture the output
	# result = subprocess.run(cmd, capture_output=True, text=True)

	# # Display the captured output
	# st.write(result.stdout)
	# from contextlib import contextmanager
	# from io import StringIO
	# from threading import current_thread
	# import streamlit as st
	# import sys

	# # Define default value for REPORT_CONTEXT_ATTR_NAME
	# REPORT_CONTEXT_ATTR_NAME = "_report_ctx"

	# @contextmanager
	# def st_redirect(src, dst):
	#     placeholder = st.empty()
	#     output_func = getattr(placeholder, dst)

	#     with StringIO() as buffer:
	#         old_write = src.write

	#         def new_write(b):
	#             if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
	#                 buffer.write(b)
	#                 output_func(buffer.getvalue())
	#             else:
	#                 old_write(b)

	#         try:
	#             src.write = new_write
	#             yield
	#         finally:
	#             src.write = old_write


	# @contextmanager
	# def st_stdout(dst):
	# 	with st_redirect(sys.stdout, dst):
	# 		print("Prints as st.coode()")
	# 		yield


	# @contextmanager
	# def st_stderr(dst):
	# 	with st_redirect(sys.stderr, dst):
	# 		print("Prints as st.coode()")
	# 		yield


	# with st_stdout("code"):
	#     print("Prints as st.code()")

	# with st_stdout("info"):
	#     print("Prints as st.info()")

	# with st_stdout("markdown"):
	#     print("Prints as st.markdown()")

	# with st_stdout("success"), st_stderr("error"):
	#     print("You can print regular success messages")
	#     print("And you can redirect errors as well at the same time", file=sys.stderr)










    # # Define the command to be executed
	# from contextlib import contextmanager, redirect_stdout
	# from io import StringIO
	# from time import sleep
	# @contextmanager
	# def st_capture(output_func):
	#     with StringIO() as stdout, redirect_stdout(stdout):
	#         old_write = stdout.write

	#         def new_write(string):
	#             ret = old_write(string)
	#             output_func(stdout.getvalue())
	#             return ret
	        
	#         stdout.write = new_write
	#         yield

	# output = st.empty()
	# with st_capture(output.code):
	# 	print(exec(grass))
	# 	print("Hello")
	# 	# sleep(1)
	# 	print("World")
	# 	print(exec(grass))
	# output = st.empty()
	# with st_capture(output.info):
	# 	print(exec(grass))
	# 	print("Goodbye")
	# 	sleep(1)
	# 	print("World")

        # Get user input using a Streamlit text_input component
        # user_input = st.text_input("Input", key='jj_input_' + str(hash(output)))

        # Pass user input to the Python program
        # if user_input:
        #     process.stdin.write(user_input + "\n")
        #     process.stdin.flush()


	# if st.button("Verified"):

		
	
	
	# "*****"
	# "## Output"

	# html = f"""
	# <html>
	#   <head>
	#     <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
	#     <script defer src="https://pyscript.net/latest/pyscript.js"></script>
	#   </head>
	#   <body>
	#     <py-script>{code}</py-script>
	#   </body>
	# </html>
	# """

	# st.components.v1.html(html, height=200, scrolling=True)
