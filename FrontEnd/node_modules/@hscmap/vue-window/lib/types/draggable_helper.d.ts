export declare type Options = {
    onMove?: () => void;
    onMoveStart?: () => void;
    onMoveEnd?: () => void;
};
export declare class DraggableHelper {
    readonly handle: HTMLElement;
    readonly container: HTMLElement;
    readonly options: Options;
    private unbindDown;
    private unbindMove?;
    private unbindUp?;
    constructor(handle: HTMLElement, container: HTMLElement, options?: Options);
    teardown(): void;
    private offsetX;
    private offsetY;
    private mousedown;
    private mousemove;
    private mouseup;
}
