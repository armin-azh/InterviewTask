import {useContext} from "react";

// Context
import {HomeContext} from "@/components/Home/Context";


// Components
import Enrollment from "@/components/Home/Enrollment";
import UploadVideo from "@/components/Home/UploadVideo";
import Persons from "@/components/Home/Persons";



export default function TabSelector() {

    const {tabId} = useContext(HomeContext);

    switch (tabId) {
        case 0:
            return <UploadVideo/>
        case 1:
            return <Enrollment/>
        case 2:
            return <Persons/>
        default:
            return null;
    }
}