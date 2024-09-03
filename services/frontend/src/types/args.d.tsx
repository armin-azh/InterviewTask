

export interface HookArgs {
    onUpdate?: () => void;
    onError?: ()=> void;
    onFinally?: ()=>void;
}


export interface PaginationArgs{
    page?: number;
    pageSize?: number;
}