export declare function isTouchEvent(e: MouseEvent | TouchEvent): e is TouchEvent;
export declare class SinglePointerEvent {
    readonly e: MouseEvent | TouchEvent;
    constructor(e: MouseEvent | TouchEvent);
    stopPropagation(): void;
    preventDefault(): void;
    get clientX(): number;
    get clientY(): number;
    get clientCoord(): V2;
    static bindDown(target: HTMLElement, cb: (e: SinglePointerEvent) => void, cancel?: (e: SinglePointerEvent) => void, useCapture?: boolean): () => void;
    static bindMove(target: HTMLElement | Document, cb: (e: SinglePointerEvent) => void, useCapture?: boolean): () => void;
    static bindUp(target: HTMLElement | Document, cb: (e: SinglePointerEvent) => void, useCapture?: boolean): () => void;
    originalEvent({ mouse, touch }: Partial<{
        mouse: (e: MouseEvent) => void;
        touch: (e: TouchEvent) => void;
    }>): void;
}
export declare class V2 {
    x: number;
    y: number;
    constructor(x: number, y: number);
    clone(): V2;
}
