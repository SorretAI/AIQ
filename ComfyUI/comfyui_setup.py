import os
import subprocess
import platform
import urllib.request
from huggingface_hub import snapshot_download

# ----------------------------
# 📦 INSTALL REQUIRED LIBRARIES
# ----------------------------
def install_required_libraries():
    print("🔧 Installing/upgrading required libraries...")
    subprocess.run(["pip", "install", "--upgrade", "huggingface_hub", "ipywidgets", "hf_transfer", "jupyterlab-widgets"])
    subprocess.run(["pip", "install", "--upgrade", "git+https://github.com/huggingface/huggingface_hub"])

# ----------------------------
# 🔐 AUTHENTICATION
# ----------------------------
def authenticate_huggingface():
    hf_token = input("🔑 Enter your Hugging Face token: ").strip()
    os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
    os.environ["HF_HUB_VERBOSITY"] = "info"

    try:
        subprocess.run(["huggingface-cli", "login", "--token", hf_token], check=True)
        print("✅ Authentication successful.")
    except subprocess.CalledProcessError:
        print("❌ Hugging Face login failed.")
    return hf_token

# ----------------------------
# 📥 HELPER DOWNLOAD FUNCTIONS
# ----------------------------
def download_file_public(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"⬇️ Downloading public URL:\n{url} → {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print("✅ Download complete.\n")
    except Exception as e:
        print(f"❌ Error downloading {url}\n{e}\n")

def download_file_with_token(url, dest_path, token):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    headers = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=headers)
    print(f"🔐 Downloading with token:\n{url} → {dest_path}")
    try:
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print("✅ Authenticated download complete.\n")
    except Exception as e:
        print(f"❌ Authenticated download failed for {url}\n{e}\n")

def download_with_wget(url, dest_dir):
    """Download using wget with content-disposition to preserve original filename"""
    os.makedirs(dest_dir, exist_ok=True)
    print(f"⬇️ Downloading with wget:\n{url} → {dest_dir}")
    try:
        # Change to destination directory and run wget
        original_dir = os.getcwd()
        os.chdir(dest_dir)
        subprocess.run(["wget", url, "--content-disposition"], check=True)
        os.chdir(original_dir)
        print("✅ Wget download complete.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Wget download failed:\n{e}\n")
    except FileNotFoundError:
        print("❌ wget command not found. Please install wget or use alternative download method.\n")

# ----------------------------
# 📁 BASE PATH SETUP
# ----------------------------
base_model_path = "/workspace/ComfyUI/models"
print(f"📁 Model base path: {base_model_path}")
os.makedirs(base_model_path, exist_ok=True)

# ----------------------------
# 🧠 HUGGING FACE MODEL DOWNLOAD FUNCTION
# ----------------------------
def download_model(repo_id, filenames, destination_subfolder):
    dest_path = os.path.join(base_model_path, destination_subfolder)
    os.makedirs(dest_path, exist_ok=True)
    print(f"📥 Downloading from {repo_id} → {dest_path}")
    try:
        snapshot_download(
            repo_id=repo_id,
            allow_patterns=filenames,
            local_dir=dest_path,
            local_dir_use_symlinks=False
        )
        print(f"✅ Downloaded {filenames} to {dest_path}\n")
    except Exception as e:
        print(f"❌ Failed to download from {repo_id}\n{e}\n")

# ----------------------------
# ✅ MAIN SCRIPT
# ----------------------------
if __name__ == "__main__":
    install_required_libraries()
    hf_token = authenticate_huggingface()

    download_file_with_token(
        "https://huggingface.co/bstungnguyen/Flux/resolve/main/flux1-dev.safetensors",
        os.path.join(base_model_path, "diffusion_models/flux1-dev.safetensors"),
        hf_token
    )
    
    download_file_with_token(
        "https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors",
        os.path.join(base_model_path, "vae/flux/ae.safetensors"),
        hf_token
    )

    download_file_with_token(
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
        os.path.join(base_model_path, "text_encoders/flux/clip_l.safetensors"),
        hf_token
    )
    download_file_with_token(
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors",
        os.path.join(base_model_path, "text_encoders/t5xxl_fp16.safetensors"),
        hf_token
    )

    download_file_with_token(
        "https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Upscaler/blob/main/diffusion_pytorch_model.safetensors",
        os.path.join(base_model_path, "controlnet/FLUX.1/jasperai-dev-Upscaler/diffusion_pytorch_model.safetensors"),
        hf_token
    )

    download_file_with_token(
        "https://huggingface.co/second-state/stable-diffusion-3.5-large-GGUF/resolve/dff185441d61601155591a46f691d7f73151acdd/clip_g.safetensors",
        os.path.join(base_model_path, "text_encoders/clip_g.safetensors"),
        hf_token
    )



    print("🎉 All model downloads completed successfully.")
    print("\n📂 Your model structure:")
    print("models/")
    print("├── 📂 diffusion_models/")
    print("│   └── flux1-dev-kontext_fp8_scaled.safetensors")
    print("├── 📂 vae/")
    print("│   └── ae.safetensors")
    print("├── 📂 text_encoders/")
    print("│   ├── clip_l.safetensors")
    print("│   └── t5xxl_fp8_e4m3fn_scaled.safetensors")
    print("├── 📂 upscale_models/")
    print("│   └── 2x_NMKD-UpgifLiteV2_210k.pth")