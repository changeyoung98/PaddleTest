#!/usr/bin/env bash

export docker_type="${docker_type:-Ubuntu}"
export cuda_ver="${cuda_ver:-cuda11.2}"

if [[ "${docker_type}" == "Ubuntu" ]];then
    case ${cuda_ver} in
    "cuda10.2")
        echo "Selected Ubuntu: Cuda10.2"
        export docker_image="registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.2-cudnn7.6-trt7.0-gcc8.2"
        ;;
    "cuda11.2")
        echo "Selected Ubuntu: Cuda11.2"
        export docker_image="registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.2-cudnn8.2-trt8.0-gcc82"
        ;;
    "cuda11.6")
        echo "Selected Ubuntu: Cuda11.6"
        export docker_image="registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.6-cudnn8.4-trt8.4-gcc82"
        ;;
    "cuda11.7")
        echo "Selected Ubuntu: Cuda11.7"
        export docker_image="registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.7-cudnn8.4-trt8.4-gcc82"
        ;;
    "cuda11.8")
        echo "Selected Ubuntu: Cuda11.8"
        export docker_image="registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.8-cudnn8.6-trt8.5-gcc82"
        ;;
    "cuda12.0")
        echo "Selected Ubuntu: Cuda12.0"
        export docker_image="registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda12.0-cudnn8.9-trt8.6-gcc12.2"
        ;;
    *)
        echo "Unknown CUDA version: ${cuda_ver}"
        exit 1
        ;;
    esac

elif [[ "${docker_type}" == "Centos" ]];then
    case ${cuda_ver} in
    "cuda10.2")
        echo "Selected Centos: Cuda102"
        export Image_version="registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda10.2-cudnn7.6-trt7.0-gcc8.2"
        ;;
    "cuda11.2")
        echo "Selected Centos: Cuda112"
        export Image_version="registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.2-cudnn8.2-trt8.0-gcc82"
        ;;
    "cuda11.6")
        echo "Selected Centos: Cuda116"
        export Image_version="registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.6-cudnn8.4-trt8.4-gcc8.2"
        ;;
    "cuda11.7")
        echo "Selected Centos: Cuda117"
        export Image_version="registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.7-cudnn8.4-trt8.4-gcc8.2"
        ;;
    "cuda11.8")
        echo "Selected Centos: Cuda118"
        export Image_version="registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.8-cudnn8.6-trt8.5-gcc8.2"
        ;;
    "cuda12.0")
        echo "Selected Centos: Cuda120"
        export Image_version="registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda12.0-cudnn8.9-trt8.6-gcc12.2"
        ;;
    *)
        echo "Unknown CUDA version: ${cuda_ver}"
        exit 1
        ;;
    esac
else
    echo "Unknown docker_type: ${docker_type}"
    exit 1
fi