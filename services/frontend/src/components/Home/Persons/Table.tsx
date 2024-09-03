import {useState, useEffect} from "react";
import {nanoid} from "nanoid";
import moment from "moment";

// Components
import Loading from "@/components/Loading";

// Hooks
import {useGetPersonsQuery} from "@/store/api/gateway";

// type
import type {PaginationArgs} from "@/types/args.d";

export default function Table() {
    const [page, setPage] = useState<PaginationArgs>({page: 1, pageSize: 10});

    const {data, isLoading, refetch} = useGetPersonsQuery(page)

    useEffect(() => {
        refetch();
    }, [page]);


    return<div className="relative overflow-x-auto rounded-lg">
        <Loading isLoading={isLoading}/>
        <table className="w-full text-sm text-left rtl:text-right text-gray-500">
            <thead className="text-xs text-white uppercase bg-blue-500">
            <tr>
                <th scope="col" className="px-6 py-3">
                    #
                </th>
                <th scope="col" className="px-6 py-3">
                    ID
                </th>
                <th scope="col" className="px-6 py-3">
                    Firstname
                </th>
                <th scope="col" className="px-6 py-3">
                    Lastname
                </th>
                <th scope="col" className="px-6 py-3">
                    Created
                </th>
            </tr>
            </thead>
            <tbody>

            {
                data?.results.map((item, index) => {
                    return <tr className="text-gray-700 border-b-2" key={nanoid()}>
                        <th scope="row"
                            className="px-6 py-4 font-medium">
                            {index + 1}
                        </th>
                        <th scope="row"
                            className="px-6 py-4 font-medium">
                            {item.prime}
                        </th>
                        <td className="px-6 py-4 capitalize">
                            {item.first_name}
                        </td>
                        <td className="px-6 py-4 capitalize">
                            {item.last_name}
                        </td>
                        <td className="px-6 py-4">
                            {moment(item.created_at.Time).format('YYYY-MM-DD HH:mm:ss A')}
                        </td>
                    </tr>
                })
            }

            </tbody>
        </table>
    </div>

}