import { API_URL } from "./constants";

export const getEndpoint = async (endpoint) => {
    try {
        const response = await axios.get(endpoint);
        return response.data
    }
    catch (error) {
        console.error('Error fetching data', error);
    }
}

export const postEndpoint = async(endpoint, data=null, config=null) => {
    try{
        const response =  await axios.post(endpoint, data=data, config=config);
    }
   catch(error){
    console.error('Error occured', error)
   }
}

export const getBackend = async(endpoint) => {
    return await getEndpoint(API_URL + endpoint)
}
export const postBackend = async(endpoint, data=null, config=null) => {
    return await postEndpoint(
        API_URL + endpoint,
        data,
        {
            headers: config.headers ?? {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer access-token'
            },
            params: config.params
        }
    )
}