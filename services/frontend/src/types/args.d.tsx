

export interface HookArgs {
    onUpdate?: () => void;
    onError?: ()=> void;
    onFinally?: ()=>void;
}


export interface PaginationArgs{
    page?: number;
    pageSize?: number;
}

export interface PrimeAndPageArgs extends PaginationArgs{
    prime: string
}
