import axios from "axios";

const baseAddress = 'http://localhost:8000';

const api = {
    image:{
        predict: (image_name, formData) => {
            return axios.post(`${baseAddress}/image_detection/${image_name}`, formData)
        },
        get_predicted: (image_name) => {
            return axios.get(`${baseAddress}/image_detection/${image_name}`)
        },
        list_images: () => {
            return axios.get(`${baseAddress}/list/image_detection/`)
        },
        delete: (image_name) => {
            return axios.delete(`${baseAddress}/image_detection/${image_name}`)
        },
    },
    video:{
        predict: (image_name, formData) => {
            return axios.post(`${baseAddress}/video_detection/${image_name}`, formData)
        },
        get_predicted: (image_name) => {
            return axios.get(`${baseAddress}/video_detection/${image_name}`)
        },
        list_videos: () => {
            return axios.get(`${baseAddress}/list/video_detection/`)
        },
        delete: (image_name) => {
            return axios.delete(`${baseAddress}/video_detection/${image_name}`)
        },
    }
}

export default api;