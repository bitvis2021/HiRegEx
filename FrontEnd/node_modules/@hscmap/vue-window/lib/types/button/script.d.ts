import { WindowStyle } from "../style";
import { Vue } from "vue-property-decorator";
export declare class Button extends Vue {
    windowStyle: WindowStyle;
    disabled: boolean;
    hover: boolean;
    active: boolean;
    get style(): Partial<CSSStyleDeclaration>;
    mousedown(e: MouseEvent & TouchEvent): void;
    mouseup(e: MouseEvent & TouchEvent): void;
}
