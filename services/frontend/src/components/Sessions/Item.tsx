
// Hooks
import {useGetPersonByIdQuery} from "@/store/api/gateway";


import type {Result} from "@/types/models/result.d";
import {nanoid} from "nanoid";

interface Props {
    data: Result
}

export default function Item(props: Props) {

    const {data} = useGetPersonByIdQuery({id: props.data.person_id})

    const url = new URL(props.data.thumbnail_path.replace("thumbnails", "media"), process.env.NEXT_PUBLIC_GW_URL || "http://localhost:8080").toString();

    return <tr className="text-gray-700 border-b-2" key={nanoid()}>
        <th scope="row"
            className="px-6 py-4 font-medium">
            <img className="w-8 h-8 rounded-full" src={url} alt="Neil image"/>
        </th>
        <th scope="row"
            className="px-6 py-4 font-medium">
            {props.data.similarity.toFixed(3)}
        </th>
        <td className="px-6 py-4 capitalize">
            {props.data.similarity >= 0.35? <span
                    className="bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded">Matched</span> :
                <span
                    className="bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded">Mismatched</span>}

        </td>
        <td className="px-6 py-4 capitalize">
            {data?.data.first_name} {data?.data.last_name}
        </td>
    </tr>

}