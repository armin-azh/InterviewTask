import { configureStore} from "@reduxjs/toolkit";

// APIs
import {gatewayApi} from "@/store/api/gateway";


export const store = configureStore({
    reducer: {
        [gatewayApi.reducerPath]: gatewayApi.reducer,

    },
    devTools: process.env.NODE_ENV !== "production",

    middleware: getDefaultMiddleware => getDefaultMiddleware()
        .concat(gatewayApi.middleware)
});