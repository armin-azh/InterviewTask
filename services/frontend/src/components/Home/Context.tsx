import {createContext} from "react";

// Types
import type {TabProp} from "@/types/pages/home.d";

// New Home context
export const HomeContext = createContext<TabProp>({tabId: 0});