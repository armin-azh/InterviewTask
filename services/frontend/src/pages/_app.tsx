import "@/styles/globals.css";
import "@/styles/toast.css";
import type { AppProps } from "next/app";

// CSS
import 'react-toastify/dist/ReactToastify.css';

// Containers
import {ToastContainer} from "react-toastify";

import {Provider } from 'react-redux';
import {store} from "@/store/store";

export default function App({ Component, pageProps }: AppProps) {
  return <Provider store={store}>
    <ToastContainer/>
    <Component {...pageProps} />;
  </Provider>;
}
