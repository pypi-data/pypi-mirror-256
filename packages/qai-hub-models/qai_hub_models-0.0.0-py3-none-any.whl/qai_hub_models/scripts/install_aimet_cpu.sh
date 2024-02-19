# AIMET installation script for Linux.
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    MSYS_NT*)   machine=Git;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ "$machine" != "Linux" ]; then
    echo "AIMET is only supported on Linux."
    exit
fi

# Install Torch CPU
pip install torch==1.13.1+cpu torchvision==0.14.1+cpu torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cpu

# Install AIMET
export AIMET_VARIANT=torch_cpu
export release_tag=1.29.0
export download_url="https://github.com/quic/aimet/releases/download/${release_tag}"
export wheel_file_suffix="cp38-cp38-linux_x86_64.whl"

pip install ${download_url}/AimetCommon-${AIMET_VARIANT}_${release_tag}-${wheel_file_suffix}
pip install ${download_url}/AimetTorch-${AIMET_VARIANT}_${release_tag}-${wheel_file_suffix} -f https://download.pytorch.org/whl/torch_stable.html
pip install ${download_url}/Aimet-${AIMET_VARIANT}_${release_tag}-${wheel_file_suffix}

# Needed for python3.8. Run sudo only if python3.8 is not found
if ! command -v python3.8 &> /dev/null
then
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
fi


site_packages=$(python -c 'import site; print(site.getsitepackages()[0])')
xargs sudo apt-get --assume-yes install < "${site_packages}/aimet_common/bin/reqs_deb_common.txt"
