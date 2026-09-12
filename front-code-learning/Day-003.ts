//TypeScript Generics

//Generic

// noe daghigh dade ra alan moshakhas ne mikonam va moghe estefadeh moshakhasesh mikonam

const apiGet = async <T>(
    url: string
): Promise<T> => {
    //
}

// T = Type


const apiGet = async <T>(url: string): Promise<T> => {
    const response = await fetch(url);

    if(!response.ok){
        throw new Error (`request failed with status ${response.status}`);
    }

    const data: T = await response.json();

    return data;
};

//

interface Property {
    id : number;
    title : string;
    price : number;
    city : string;
    isActive : boolean;
}

const property = await apiGet<Property>("/api/properties/42");



// any khob nist chon typescript on vaght chizi nemige



class ApiError extends Error { // error sefareshi sakhtim va az error asli javascript ers bari mikone
    status: number; // yek property jadid be error ezafe mikoone
    constructor(message: string, status: number) { // line 60
        super(message);

        this.name = "ApiError";
        this.status = status;
    }
}

const apiGet = async <T>(url: string): Promise<T> => {
    const response = await fetch(url);

    if(!response.ok){
        throw new ApiError(`Request failed ${response.statusText}`, response.status));
    }

    const data: T = await response.json();

    return data;
};
