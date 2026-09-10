//Api manegment try/catch


const response = await fetch (`/api/properties/${id}`);

//fetch error : internet disconnect , Server unavailable , DNS error , Request aborted.

//Server response : 404 Not Found , 401 Unauthorized , 500 Internal Server Error.

if (!response.ok) {
    throw new Error ("Failed to fetch property");
}

//upper

interface Property {
    id : number ;
    title : string;
    price : number;
    city: string;
    iActive : boolean;
}

const getProperty = async (id: number) : Promise<Property> => {
    try { //kod hayee ke momken hast error bedahand ra dakhele in belak ejra kon
        const response = await fetch(`/api/properties/${id}`);

        if (!response.ok) { //True: 200 , 201 , 204    False: 400 , 401 , 403 , 404 , 500
            throw new Error (`Failed to fetch property. status : ${response.status}`);
        }

        const property: Property = await response.json();

        return property;
    } catch (error) {
        console.error("getProperty error:", error);

        throw error;
    }
};

//exercise

interface User {
    id : number;
    name: string;
    email: string;
    isActive: boolean;
}

const getuser = async (id: number): Promise<User> => {
    try{
        const response = await fetch (`/api/user/${id}`);

        if (!response.ok) {
            throw new Error (`Failed to fetch user. status: ${response.status}`);
        }

        const user: User = await response.json();

        return user;
    }catch (error) {
        console.error("getuser error",error);
        
        throw error;
    }
}