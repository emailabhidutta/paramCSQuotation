import {
  DomSanitizer
} from "./chunk-5SIMKGIY.js";
import {
  NgClass
} from "./chunk-GWAU3GAC.js";
import {
  Component,
  Directive,
  ElementRef,
  HostBinding,
  Injectable,
  Input,
  NgModule,
  Optional,
  Renderer2,
  SkipSelf,
  ViewChild,
  afterNextRender,
  computed,
  inject,
  setClassMetadata,
  signal,
  ɵɵInputTransformsFeature,
  ɵɵStandaloneFeature,
  ɵɵadvance,
  ɵɵattribute,
  ɵɵclassMap,
  ɵɵconditional,
  ɵɵdefineComponent,
  ɵɵdefineDirective,
  ɵɵdefineInjectable,
  ɵɵdefineInjector,
  ɵɵdefineNgModule,
  ɵɵdirectiveInject,
  ɵɵelement,
  ɵɵelementEnd,
  ɵɵelementStart,
  ɵɵhostProperty,
  ɵɵinject,
  ɵɵloadQuery,
  ɵɵnamespaceSVG,
  ɵɵnextContext,
  ɵɵproperty,
  ɵɵqueryRefresh,
  ɵɵsanitizeHtml,
  ɵɵtemplate,
  ɵɵviewQuery
} from "./chunk-ADJ6LL3Q.js";

// node_modules/@coreui/icons-angular/fesm2022/coreui-icons-angular.mjs
var _c0 = ["svgElement"];
function IconComponent_Conditional_0_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵnamespaceSVG();
    ɵɵelement(0, "svg", 1, 0);
  }
  if (rf & 2) {
    const ctx_r0 = ɵɵnextContext();
    ɵɵproperty("innerHtml", ctx_r0.innerHtml(), ɵɵsanitizeHtml)("ngClass", ctx_r0.computedClasses)("cHtmlAttr", ctx_r0.attributes);
    ɵɵattribute("width", ctx_r0.width)("height", ctx_r0.height || ctx_r0.width)("viewBox", ctx_r0.viewBox);
  }
}
function IconComponent_Conditional_1_Template(rf, ctx) {
  if (rf & 1) {
    ɵɵnamespaceSVG();
    ɵɵelementStart(0, "svg", 2, 0);
    ɵɵelement(2, "use");
    ɵɵelementEnd();
  }
  if (rf & 2) {
    const ctx_r0 = ɵɵnextContext();
    ɵɵproperty("ngClass", ctx_r0.computedClasses)("cHtmlAttr", ctx_r0.attributes);
    ɵɵattribute("width", ctx_r0.width)("height", ctx_r0.height || ctx_r0.width);
    ɵɵadvance(2);
    ɵɵattribute("href", ctx_r0.use);
  }
}
var IconSetService = class _IconSetService {
  constructor() {
    this._iconNames = {};
    this._icons = {};
  }
  get iconNames() {
    return this._iconNames;
  }
  get icons() {
    return this._icons;
  }
  set icons(iconSet) {
    for (const iconsKey in iconSet) {
      this._iconNames[iconsKey] = iconsKey;
    }
    this._icons = iconSet;
  }
  getIcon(name) {
    const icon = this.icons[name];
    if (!icon) {
      console.warn(`CoreUI WARN: Icon ${name} is not registered in IconService`);
    }
    return this.icons[name];
  }
  static {
    this.ɵfac = function IconSetService_Factory(__ngFactoryType__) {
      return new (__ngFactoryType__ || _IconSetService)();
    };
  }
  static {
    this.ɵprov = ɵɵdefineInjectable({
      token: _IconSetService,
      factory: _IconSetService.ɵfac,
      providedIn: "root"
    });
  }
};
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(IconSetService, [{
    type: Injectable,
    args: [{
      providedIn: "root"
    }]
  }], null, null);
})();
var IconSetModule = class _IconSetModule {
  constructor(parentModule) {
    if (parentModule) {
      throw new Error("CoreUI IconSetModule is already loaded. Import it in the AppModule only");
    }
  }
  static forRoot() {
    return {
      ngModule: _IconSetModule,
      providers: [{
        provide: IconSetService
      }]
    };
  }
  static {
    this.ɵfac = function IconSetModule_Factory(__ngFactoryType__) {
      return new (__ngFactoryType__ || _IconSetModule)(ɵɵinject(_IconSetModule, 12));
    };
  }
  static {
    this.ɵmod = ɵɵdefineNgModule({
      type: _IconSetModule
    });
  }
  static {
    this.ɵinj = ɵɵdefineInjector({
      providers: [IconSetService]
    });
  }
};
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(IconSetModule, [{
    type: NgModule,
    args: [{
      providers: [IconSetService]
    }]
  }], () => [{
    type: IconSetModule,
    decorators: [{
      type: Optional
    }, {
      type: SkipSelf
    }]
  }], null);
})();
function toCamelCase(value) {
  return value.replace(/([-_][a-z0-9])/ig, ($1) => {
    return $1.toUpperCase().replace("-", "");
  });
}
function transformName(value) {
  return value && value.includes("-") ? toCamelCase(value) : value;
}
var IconDirective = class _IconDirective {
  #elementRef;
  #sanitizer;
  #iconSet;
  constructor() {
    this.#elementRef = inject(ElementRef);
    this.#sanitizer = inject(DomSanitizer);
    this.#iconSet = inject(IconSetService);
    this.#content = signal("");
    this.size = "";
    this.#name = signal("");
    this.ariaHidden = true;
    this.xmlns = "http://www.w3.org/2000/svg";
    this.pointerEvents = "none";
    this.role = "img";
    this.innerHtml = computed(() => {
      const code = Array.isArray(this.code()) ? this.code()[1] ?? this.code()[0] ?? "" : this.code() || "";
      return this.#sanitizer.bypassSecurityTrustHtml(this.titleCode + code || "");
    });
    this.code = computed(() => {
      if (this.#content()) {
        return this.#content();
      }
      if (this.#iconSet && this.#name()) {
        return this.#iconSet.getIcon(this.#name());
      }
      if (this.#name() && !this.#iconSet?.icons[this.#name()]) {
        console.warn(`cIcon directive: The '${this.#name()}' icon not found. Add it to the IconSet service for use with the 'name' property. 
`, this.#name());
      }
      return "";
    });
    this.scale = computed(() => {
      return Array.isArray(this.code()) && (this.code()?.length ?? 0) > 1 ? `0 0 ${this.code()?.[0]}` : "0 0 64 64";
    });
    afterNextRender({
      write: () => {
        this.#elementRef.nativeElement.innerHTML = this.innerHtml();
      }
    });
  }
  set content(value) {
    this.#content.set(value);
  }
  #content;
  set name(value) {
    this.#name.set(value);
  }
  get name() {
    return this.#name();
  }
  #name;
  set viewBox(viewBox) {
    this._viewBox = viewBox;
  }
  get viewBox() {
    return this._viewBox ?? this.scale();
  }
  get hostClasses() {
    return this.computedClasses;
  }
  get titleCode() {
    return this.title ? `<title>${this.title}</title>` : "";
  }
  get computedSize() {
    const addCustom = !this.size && (this.width || this.height);
    return this.size === "custom" || addCustom ? "custom-size" : this.size;
  }
  get computedClasses() {
    const classes = {
      icon: true,
      [`icon-${this.computedSize}`]: !!this.computedSize
    };
    return this.customClasses ?? classes;
  }
  static {
    this.ɵfac = function IconDirective_Factory(__ngFactoryType__) {
      return new (__ngFactoryType__ || _IconDirective)();
    };
  }
  static {
    this.ɵdir = ɵɵdefineDirective({
      type: _IconDirective,
      selectors: [["svg", "cIcon", ""]],
      hostAttrs: ["ngSkipHydration", "true"],
      hostVars: 8,
      hostBindings: function IconDirective_HostBindings(rf, ctx) {
        if (rf & 2) {
          ɵɵhostProperty("innerHtml", ctx.innerHtml(), ɵɵsanitizeHtml);
          ɵɵattribute("viewBox", ctx.viewBox)("aria-hidden", ctx.ariaHidden)("xmlns", ctx.xmlns)("pointer-events", ctx.pointerEvents)("role", ctx.role);
          ɵɵclassMap(ctx.hostClasses);
        }
      },
      inputs: {
        content: [0, "cIcon", "content"],
        customClasses: "customClasses",
        size: "size",
        title: "title",
        height: "height",
        width: "width",
        name: [2, "name", "name", transformName],
        viewBox: "viewBox",
        xmlns: "xmlns",
        pointerEvents: [0, "pointer-events", "pointerEvents"],
        role: "role"
      },
      exportAs: ["cIcon"],
      standalone: true,
      features: [ɵɵInputTransformsFeature]
    });
  }
};
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(IconDirective, [{
    type: Directive,
    args: [{
      exportAs: "cIcon",
      selector: "svg[cIcon]",
      standalone: true,
      host: {
        ngSkipHydration: "true",
        "[innerHtml]": "innerHtml()"
      }
    }]
  }], () => [], {
    content: [{
      type: Input,
      args: ["cIcon"]
    }],
    customClasses: [{
      type: Input
    }],
    size: [{
      type: Input
    }],
    title: [{
      type: Input
    }],
    height: [{
      type: Input
    }],
    width: [{
      type: Input
    }],
    name: [{
      type: Input,
      args: [{
        transform: transformName
      }]
    }],
    viewBox: [{
      type: HostBinding,
      args: ["attr.viewBox"]
    }, {
      type: Input
    }],
    ariaHidden: [{
      type: HostBinding,
      args: ["attr.aria-hidden"]
    }],
    xmlns: [{
      type: HostBinding,
      args: ["attr.xmlns"]
    }, {
      type: Input
    }],
    pointerEvents: [{
      type: HostBinding,
      args: ["attr.pointer-events"]
    }, {
      type: Input,
      args: ["pointer-events"]
    }],
    role: [{
      type: HostBinding,
      args: ["attr.role"]
    }, {
      type: Input
    }],
    hostClasses: [{
      type: HostBinding,
      args: ["class"]
    }]
  });
})();
var HtmlAttributesDirective = class _HtmlAttributesDirective {
  constructor(renderer, el) {
    this.renderer = renderer;
    this.el = el;
  }
  ngOnInit() {
    const attribs = this.cHtmlAttr;
    for (const attr in attribs) {
      if (attr === "style" && typeof attribs[attr] === "object") {
        this.setStyle(attribs[attr]);
      } else if (attr === "class") {
        this.addClass(attribs[attr]);
      } else {
        this.setAttrib(attr, attribs[attr]);
      }
    }
  }
  setStyle(styles) {
    for (const style in styles) {
      if (style) {
        this.renderer.setStyle(this.el.nativeElement, style, styles[style]);
      }
    }
  }
  addClass(classes) {
    const classArray = Array.isArray(classes) ? classes : classes.split(" ");
    classArray.filter((element) => element.length > 0).forEach((element) => {
      this.renderer.addClass(this.el.nativeElement, element);
    });
  }
  setAttrib(key, value) {
    value !== null ? this.renderer.setAttribute(this.el.nativeElement, key, value) : this.renderer.removeAttribute(this.el.nativeElement, key);
  }
  static {
    this.ɵfac = function HtmlAttributesDirective_Factory(__ngFactoryType__) {
      return new (__ngFactoryType__ || _HtmlAttributesDirective)(ɵɵdirectiveInject(Renderer2), ɵɵdirectiveInject(ElementRef));
    };
  }
  static {
    this.ɵdir = ɵɵdefineDirective({
      type: _HtmlAttributesDirective,
      selectors: [["", "cHtmlAttr", ""]],
      inputs: {
        cHtmlAttr: "cHtmlAttr"
      },
      exportAs: ["cHtmlAttr"],
      standalone: true
    });
  }
};
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(HtmlAttributesDirective, [{
    type: Directive,
    args: [{
      selector: "[cHtmlAttr]",
      exportAs: "cHtmlAttr",
      standalone: true
    }]
  }], () => [{
    type: Renderer2
  }, {
    type: ElementRef
  }], {
    cHtmlAttr: [{
      type: Input
    }]
  });
})();
var IconComponent = class _IconComponent {
  #renderer;
  #elementRef;
  #sanitizer;
  #iconSet;
  constructor() {
    this.#renderer = inject(Renderer2);
    this.#elementRef = inject(ElementRef);
    this.#sanitizer = inject(DomSanitizer);
    this.#iconSet = inject(IconSetService);
    this.#content = signal("");
    this.attributes = {
      role: "img"
    };
    this.size = "";
    this.use = "";
    this.#name = signal("");
    this.innerHtml = computed(() => {
      const code = Array.isArray(this.code()) ? this.code()[1] ?? this.code()[0] ?? "" : this.code() || "";
      return this.#sanitizer.bypassSecurityTrustHtml(this.titleCode + code || "");
    });
    this.code = computed(() => {
      if (this.#content()) {
        return this.#content();
      }
      if (this.#iconSet && this.#name()) {
        return this.#iconSet.getIcon(this.#name());
      }
      if (this.#name() && !this.#iconSet?.icons[this.#name()]) {
        console.warn(`c-icon component: icon name '${this.#name()}' does not exist for IconSet service. To use icon by 'name' prop you need to add it to IconSet service. 
`, this.#name());
      }
      return "";
    });
    this.scale = computed(() => {
      return Array.isArray(this.code()) && this.code().length > 1 ? `0 0 ${this.code()[0]}` : "0 0 64 64";
    });
    this.#renderer.setStyle(this.#elementRef.nativeElement, "display", "none");
  }
  set content(value) {
    this.#content.set(value);
  }
  #content;
  set name(value) {
    this.#name.set(value);
  }
  get name() {
    return this.#name();
  }
  #name;
  set viewBox(viewBox) {
    this._viewBox = viewBox;
  }
  get viewBox() {
    return this._viewBox ?? this.scale();
  }
  ngAfterViewInit() {
    this.#elementRef.nativeElement.classList.forEach((item) => {
      this.#renderer.addClass(this.svgElementRef.nativeElement, item);
    });
    const parentElement = this.#renderer.parentNode(this.#elementRef.nativeElement);
    const svgElement = this.svgElementRef.nativeElement;
    this.#renderer.insertBefore(parentElement, svgElement, this.#elementRef.nativeElement);
    this.#renderer.removeChild(parentElement, this.#elementRef.nativeElement);
  }
  get titleCode() {
    return this.title ? `<title>${this.title}</title>` : "";
  }
  get computedSize() {
    const addCustom = !this.size && (this.width || this.height);
    return this.size === "custom" || addCustom ? "custom-size" : this.size;
  }
  get computedClasses() {
    const classes = {
      icon: true,
      [`icon-${this.computedSize}`]: !!this.computedSize
    };
    return this.customClasses ?? classes;
  }
  static {
    this.ɵfac = function IconComponent_Factory(__ngFactoryType__) {
      return new (__ngFactoryType__ || _IconComponent)();
    };
  }
  static {
    this.ɵcmp = ɵɵdefineComponent({
      type: _IconComponent,
      selectors: [["c-icon"]],
      viewQuery: function IconComponent_Query(rf, ctx) {
        if (rf & 1) {
          ɵɵviewQuery(_c0, 5, ElementRef);
        }
        if (rf & 2) {
          let _t;
          ɵɵqueryRefresh(_t = ɵɵloadQuery()) && (ctx.svgElementRef = _t.first);
        }
      },
      hostAttrs: ["ngSkipHydration", "true"],
      inputs: {
        content: "content",
        attributes: "attributes",
        customClasses: "customClasses",
        size: "size",
        title: "title",
        use: "use",
        height: "height",
        width: "width",
        name: [2, "name", "name", transformName],
        viewBox: "viewBox"
      },
      exportAs: ["cIconComponent"],
      standalone: true,
      features: [ɵɵInputTransformsFeature, ɵɵStandaloneFeature],
      decls: 2,
      vars: 1,
      consts: [["svgElement", ""], ["xmlns", "http://www.w3.org/2000/svg", "aria-hidden", "true", "pointer-events", "none", "role", "img", 3, "innerHtml", "ngClass", "cHtmlAttr"], ["xmlns", "http://www.w3.org/2000/svg", "aria-hidden", "true", "pointer-events", "none", "role", "img", 3, "ngClass", "cHtmlAttr"]],
      template: function IconComponent_Template(rf, ctx) {
        if (rf & 1) {
          ɵɵtemplate(0, IconComponent_Conditional_0_Template, 2, 6, ":svg:svg", 1)(1, IconComponent_Conditional_1_Template, 3, 5, ":svg:svg", 2);
        }
        if (rf & 2) {
          ɵɵconditional(!ctx.use && !!ctx.code ? 0 : ctx.use ? 1 : -1);
        }
      },
      dependencies: [NgClass, HtmlAttributesDirective],
      styles: [".icon[_ngcontent-%COMP%]{display:inline-block;color:inherit;text-align:center;vertical-align:-.125rem;fill:currentColor}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size){width:1rem;height:1rem;font-size:1rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-xxl{width:2rem;height:2rem;font-size:2rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-xl{width:1.5rem;height:1.5rem;font-size:1.5rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-lg{width:1.25rem;height:1.25rem;font-size:1.25rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-sm{width:.875rem;height:.875rem;font-size:.875rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-3xl{width:3rem;height:3rem;font-size:3rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-4xl{width:4rem;height:4rem;font-size:4rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-5xl{width:5rem;height:5rem;font-size:5rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-6xl{width:6rem;height:6rem;font-size:6rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-7xl{width:7rem;height:7rem;font-size:7rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-8xl{width:8rem;height:8rem;font-size:8rem}.icon[_ngcontent-%COMP%]:not(.icon-c-s):not(.icon-custom-size).icon-9xl{width:9rem;height:9rem;font-size:9rem}"]
    });
  }
};
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(IconComponent, [{
    type: Component,
    args: [{
      exportAs: "cIconComponent",
      imports: [NgClass, HtmlAttributesDirective],
      selector: "c-icon",
      standalone: true,
      host: {
        ngSkipHydration: "true"
      },
      template: '@if (!use && !!code) {\n  <svg\n    xmlns="http://www.w3.org/2000/svg"\n    [attr.width]="width"\n    [attr.height]="height || width"\n    [attr.viewBox]="viewBox"\n    [innerHtml]="innerHtml()"\n    [ngClass]="computedClasses"\n    [cHtmlAttr]="attributes"\n    aria-hidden="true"\n    pointer-events="none"\n    role="img"\n    #svgElement\n  >\n  </svg>\n} @else if (use) {\n  <svg\n    xmlns="http://www.w3.org/2000/svg"\n    [attr.width]="width"\n    [attr.height]="height || width"\n    [ngClass]="computedClasses"\n    [cHtmlAttr]="attributes"\n    aria-hidden="true"\n    pointer-events="none"\n    role="img"\n    #svgElement\n  >\n    <use [attr.href]="use"></use>\n  </svg>\n}\n',
      styles: [".icon{display:inline-block;color:inherit;text-align:center;vertical-align:-.125rem;fill:currentColor}.icon:not(.icon-c-s):not(.icon-custom-size){width:1rem;height:1rem;font-size:1rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-xxl{width:2rem;height:2rem;font-size:2rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-xl{width:1.5rem;height:1.5rem;font-size:1.5rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-lg{width:1.25rem;height:1.25rem;font-size:1.25rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-sm{width:.875rem;height:.875rem;font-size:.875rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-3xl{width:3rem;height:3rem;font-size:3rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-4xl{width:4rem;height:4rem;font-size:4rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-5xl{width:5rem;height:5rem;font-size:5rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-6xl{width:6rem;height:6rem;font-size:6rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-7xl{width:7rem;height:7rem;font-size:7rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-8xl{width:8rem;height:8rem;font-size:8rem}.icon:not(.icon-c-s):not(.icon-custom-size).icon-9xl{width:9rem;height:9rem;font-size:9rem}\n"]
    }]
  }], () => [], {
    content: [{
      type: Input
    }],
    attributes: [{
      type: Input
    }],
    customClasses: [{
      type: Input
    }],
    size: [{
      type: Input
    }],
    title: [{
      type: Input
    }],
    use: [{
      type: Input
    }],
    height: [{
      type: Input
    }],
    width: [{
      type: Input
    }],
    name: [{
      type: Input,
      args: [{
        transform: transformName
      }]
    }],
    viewBox: [{
      type: Input
    }],
    svgElementRef: [{
      type: ViewChild,
      args: ["svgElement", {
        read: ElementRef
      }]
    }]
  });
})();
var IconModule = class _IconModule {
  static {
    this.ɵfac = function IconModule_Factory(__ngFactoryType__) {
      return new (__ngFactoryType__ || _IconModule)();
    };
  }
  static {
    this.ɵmod = ɵɵdefineNgModule({
      type: _IconModule,
      imports: [IconComponent, IconDirective],
      exports: [IconComponent, IconDirective]
    });
  }
  static {
    this.ɵinj = ɵɵdefineInjector({});
  }
};
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(IconModule, [{
    type: NgModule,
    args: [{
      imports: [IconComponent, IconDirective],
      exports: [IconComponent, IconDirective]
    }]
  }], null, null);
})();

export {
  IconSetService,
  IconSetModule,
  IconDirective,
  IconComponent,
  IconModule
};
//# sourceMappingURL=chunk-RJGIWGGE.js.map
