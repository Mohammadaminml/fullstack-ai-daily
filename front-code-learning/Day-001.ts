/* TypeScript: type safety in API*/


// Backend response API 


/*{
    id: 42,
    name: "Mohammad Amin",
    email: "example@email.com",
    role: "admin"
}*/


interface User {
    id: number;
    name: string;
    email: string ;
    role: "admin" | "user";
}

const getuser = async (id: number): Promise<User> => { /* getuser("42"*/  /* Promise<user> = asynchronous = "montazer anjam yek kar zamanbar mimone bedon inke ejraye baghie barnama ro motevaghef kone*/
    const response = await fetch (`/api/users/${id}`); /* await = "darkhast ro be API befrest va ghable as edame hamin tabe montazer natijash bemoon"*/

    if (!response.ok) {
        throw new Error ("Failed to fetch user");
    }

    const user: User = await response.json();

    return user;
}

// exercise
/*9/10*/
interface Property {
    id: number;
    title: string;
    price: number;
    city: string;
    isActive: boolean;
}

const getProperty = async (id: number): Promise<Property> => {
    const response = await fetch (`/api/getproperty/${id}`);

    if (!response.ok) {
        throw new Error ("Failed to fetch getProperty");
    }

    const getProperty: Property = await response.json();

    return getProperty;
}


/* clean code*/
interface Property {
    id: number;
    title: string;
    price: number;
    city: string;
    isActive: boolean;
}

const getProperty = async (id: number) : Promise<Property> => {
    const response = await fetch(`/api/getproperty/${id}`);

    if (!response.ok) {
        throw new Error ("Failed to fetch property");        
    }

    const property: Property = await response.json();

    return property;
}