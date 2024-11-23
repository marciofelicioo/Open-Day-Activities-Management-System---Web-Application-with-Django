/*! Buefy v0.8.16 | MIT License | github.com/buefy/buefy */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (global = global || self, factory(global.Steps = {}));
}(this, function (exports) { 'use strict';

  function _typeof(obj) {
    "@babel/helpers - typeof";

    if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
      _typeof = function (obj) {
        return typeof obj;
      };
    } else {
      _typeof = function (obj) {
        return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
      };
    }

    return _typeof(obj);
  }

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function ownKeys(object, enumerableOnly) {
    var keys = Object.keys(object);

    if (Object.getOwnPropertySymbols) {
      var symbols = Object.getOwnPropertySymbols(object);
      if (enumerableOnly) symbols = symbols.filter(function (sym) {
        return Object.getOwnPropertyDescriptor(object, sym).enumerable;
      });
      keys.push.apply(keys, symbols);
    }

    return keys;
  }

  function _objectSpread2(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {};

      if (i % 2) {
        ownKeys(Object(source), true).forEach(function (key) {
          _defineProperty(target, key, source[key]);
        });
      } else if (Object.getOwnPropertyDescriptors) {
        Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
      } else {
        ownKeys(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
    }

    return target;
  }

  function _toArray(arr) {
    return _arrayWithHoles(arr) || _iterableToArray(arr) || _nonIterableRest();
  }

  function _arrayWithHoles(arr) {
    if (Array.isArray(arr)) return arr;
  }

  function _iterableToArray(iter) {
    if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter);
  }

  function _nonIterableRest() {
    throw new TypeError("Invalid attempt to destructure non-iterable instance");
  }

  var config = {
    defaultContainerElement: null,
    defaultIconPack: 'mdi',
    defaultIconComponent: null,
    defaultIconPrev: 'chevron-left',
    defaultIconNext: 'chevron-right',
    defaultDialogConfirmText: null,
    defaultDialogCancelText: null,
    defaultSnackbarDuration: 3500,
    defaultSnackbarPosition: null,
    defaultToastDuration: 2000,
    defaultToastPosition: null,
    defaultNotificationDuration: 2000,
    defaultNotificationPosition: null,
    defaultTooltipType: 'is-primary',
    defaultTooltipAnimated: false,
    defaultTooltipDelay: 0,
    defaultInputAutocomplete: 'on',
    defaultDateFormatter: null,
    defaultDateParser: null,
    defaultDateCreator: null,
    defaultTimeCreator: null,
    defaultDayNames: null,
    defaultMonthNames: null,
    defaultFirstDayOfWeek: null,
    defaultUnselectableDaysOfWeek: null,
    defaultTimeFormatter: null,
    defaultTimeParser: null,
    defaultModalCanCancel: ['escape', 'x', 'outside', 'button'],
    defaultModalScroll: null,
    defaultDatepickerMobileNative: true,
    defaultTimepickerMobileNative: true,
    defaultNoticeQueue: true,
    defaultInputHasCounter: true,
    defaultTaginputHasCounter: true,
    defaultUseHtml5Validation: true,
    defaultDropdownMobileModal: true,
    defaultFieldLabelPosition: null,
    defaultDatepickerYearsRange: [-100, 3],
    defaultDatepickerNearbyMonthDays: true,
    defaultDatepickerNearbySelectableMonthDays: false,
    defaultDatepickerShowWeekNumber: false,
    defaultDatepickerMobileModal: true,
    defaultTrapFocus: true,
    defaultButtonRounded: false,
    defaultCarouselInterval: 3500,
    defaultLinkTags: ['a', 'button', 'input', 'router-link', 'nuxt-link', 'n-link', 'RouterLink', 'NuxtLink', 'NLink'],
    customIconPacks: null
  };

  /**
   * Merge function to replace Object.assign with deep merging possibility
   */

  var isObject = function isObject(item) {
    return _typeof(item) === 'object' && !Array.isArray(item);
  };

  var mergeFn = function mergeFn(target, source) {
    var deep = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

    if (deep || !Object.assign) {
      var isDeep = function isDeep(prop) {
        return isObject(source[prop]) && target !== null && target.hasOwnProperty(prop) && isObject(target[prop]);
      };

      var replaced = Object.getOwnPropertyNames(source).map(function (prop) {
        return _defineProperty({}, prop, isDeep(prop) ? mergeFn(target[prop], source[prop], deep) : source[prop]);
      }).reduce(function (a, b) {
        return _objectSpread2({}, a, {}, b);
      }, {});
      return _objectSpread2({}, target, {}, replaced);
    } else {
      return Object.assign(target, source);
    }
  };

  var merge = mergeFn;
  function isVueComponent(c) {
    return c && c._isVue;
  }

  var mdiIcons = {
    sizes: {
      'default': 'mdi-24px',
      'is-small': null,
      'is-medium': 'mdi-36px',
      'is-large': 'mdi-48px'
    },
    iconPrefix: 'mdi-'
  };

  var faIcons = function faIcons() {
    var faIconPrefix = config && config.defaultIconComponent ? '' : 'fa-';
    return {
      sizes: {
        'default': null,
        'is-small': null,
        'is-medium': faIconPrefix + 'lg',
        'is-large': faIconPrefix + '2x'
      },
      iconPrefix: faIconPrefix,
      internalIcons: {
        'information': 'info-circle',
        'alert': 'exclamation-triangle',
        'alert-circle': 'exclamation-circle',
        'chevron-right': 'angle-right',
        'chevron-left': 'angle-left',
        'chevron-down': 'angle-down',
        'eye-off': 'eye-slash',
        'menu-down': 'caret-down',
        'menu-up': 'caret-up',
        'close-circle': 'times-circle'
      }
    };
  };

  var getIcons = function getIcons() {
    var icons = {
      mdi: mdiIcons,
      fa: faIcons(),
      fas: faIcons(),
      far: faIcons(),
      fad: faIcons(),
      fab: faIcons(),
      fal: faIcons()
    };

    if (config && config.customIconPacks) {
      icons = merge(icons, config.customIconPacks, true);
    }

    return icons;
  };

  var script = {
    name: 'BIcon',
    props: {
      type: [String, Object],
      component: String,
      pack: String,
      icon: String,
      size: String,
      customSize: String,
      customClass: String,
      both: Boolean // This is used internally to show both MDI and FA icon

    },
    computed: {
      iconConfig: function iconConfig() {
        var allIcons = getIcons();
        return allIcons[this.newPack];
      },
      iconPrefix: function iconPrefix() {
        if (this.iconConfig && this.iconConfig.iconPrefix) {
          return this.iconConfig.iconPrefix;
        }

        return '';
      },

      /**
      * Internal icon name based on the pack.
      * If pack is 'fa', gets the equivalent FA icon name of the MDI,
      * internal icons are always MDI.
      */
      newIcon: function newIcon() {
        return "".concat(this.iconPrefix).concat(this.getEquivalentIconOf(this.icon));
      },
      newPack: function newPack() {
        return this.pack || config.defaultIconPack;
      },
      newType: function newType() {
        if (!this.type) return;
        var splitType = [];

        if (typeof this.type === 'string') {
          splitType = this.type.split('-');
        } else {
          for (var key in this.type) {
            if (this.type[key]) {
              splitType = key.split('-');
              break;
            }
          }
        }

        if (splitType.length <= 1) return;

        var _splitType = splitType,
            _splitType2 = _toArray(_splitType),
            type = _splitType2.slice(1);

        return "has-text-".concat(type.join('-'));
      },
      newCustomSize: function newCustomSize() {
        return this.customSize || this.customSizeByPack;
      },
      customSizeByPack: function customSizeByPack() {
        if (this.iconConfig && this.iconConfig.sizes) {
          if (this.size && this.iconConfig.sizes[this.size] !== undefined) {
            return this.iconConfig.sizes[this.size];
          } else if (this.iconConfig.sizes.default) {
            return this.iconConfig.sizes.default;
          }
        }

        return null;
      },
      useIconComponent: function useIconComponent() {
        return this.component || config.defaultIconComponent;
      }
    },
    methods: {
      /**
      * Equivalent icon name of the MDI.
      */
      getEquivalentIconOf: function getEquivalentIconOf(value) {
        // Only transform the class if the both prop is set to true
        if (!this.both) {
          return value;
        }

        if (this.iconConfig && this.iconConfig.internalIcons && this.iconConfig.internalIcons[value]) {
          return this.iconConfig.internalIcons[value];
        }

        return value;
      }
    }
  };

  function normalizeComponent(template, style, script, scopeId, isFunctionalTemplate, moduleIdentifier
  /* server only */
  , shadowMode, createInjector, createInjectorSSR, createInjectorShadow) {
    if (typeof shadowMode !== 'boolean') {
      createInjectorSSR = createInjector;
      createInjector = shadowMode;
      shadowMode = false;
    } // Vue.extend constructor export interop.


    var options = typeof script === 'function' ? script.options : script; // render functions

    if (template && template.render) {
      options.render = template.render;
      options.staticRenderFns = template.staticRenderFns;
      options._compiled = true; // functional template

      if (isFunctionalTemplate) {
        options.functional = true;
      }
    } // scopedId


    if (scopeId) {
      options._scopeId = scopeId;
    }

    var hook;

    if (moduleIdentifier) {
      // server build
      hook = function hook(context) {
        // 2.3 injection
        context = context || // cached call
        this.$vnode && this.$vnode.ssrContext || // stateful
        this.parent && this.parent.$vnode && this.parent.$vnode.ssrContext; // functional
        // 2.2 with runInNewContext: true

        if (!context && typeof __VUE_SSR_CONTEXT__ !== 'undefined') {
          context = __VUE_SSR_CONTEXT__;
        } // inject component styles


        if (style) {
          style.call(this, createInjectorSSR(context));
        } // register component module identifier for async chunk inference


        if (context && context._registeredComponents) {
          context._registeredComponents.add(moduleIdentifier);
        }
      }; // used by ssr in case component is cached and beforeCreate
      // never gets called


      options._ssrRegister = hook;
    } else if (style) {
      hook = shadowMode ? function () {
        style.call(this, createInjectorShadow(this.$root.$options.shadowRoot));
      } : function (context) {
        style.call(this, createInjector(context));
      };
    }

    if (hook) {
      if (options.functional) {
        // register for functional component in vue file
        var originalRender = options.render;

        options.render = function renderWithStyleInjection(h, context) {
          hook.call(context);
          return originalRender(h, context);
        };
      } else {
        // inject component registration as beforeCreate hook
        var existing = options.beforeCreate;
        options.beforeCreate = existing ? [].concat(existing, hook) : [hook];
      }
    }

    return script;
  }

  var normalizeComponent_1 = normalizeComponent;

  /* script */
  const __vue_script__ = script;

  /* template */
  var __vue_render__ = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('span',{staticClass:"icon",class:[_vm.newType, _vm.size]},[(!_vm.useIconComponent)?_c('i',{class:[_vm.newPack, _vm.newIcon, _vm.newCustomSize, _vm.customClass]}):_c(_vm.useIconComponent,{tag:"component",class:[_vm.customClass],attrs:{"icon":[_vm.newPack, _vm.newIcon],"size":_vm.newCustomSize}})],1)};
  var __vue_staticRenderFns__ = [];

    /* style */
    const __vue_inject_styles__ = undefined;
    /* scoped */
    const __vue_scope_id__ = undefined;
    /* module identifier */
    const __vue_module_identifier__ = undefined;
    /* functional template */
    const __vue_is_functional_template__ = false;
    /* style inject */
    
    /* style inject SSR */
    

    
    var Icon = normalizeComponent_1(
      { render: __vue_render__, staticRenderFns: __vue_staticRenderFns__ },
      __vue_inject_styles__,
      __vue_script__,
      __vue_scope_id__,
      __vue_is_functional_template__,
      __vue_module_identifier__,
      undefined,
      undefined
    );

  var SlotComponent = {
    name: 'BSlotComponent',
    props: {
      component: {
        type: Object,
        required: true
      },
      name: {
        type: String,
        default: 'default'
      },
      scoped: {
        type: Boolean
      },
      props: {
        type: Object
      },
      tag: {
        type: String,
        default: 'div'
      },
      event: {
        type: String,
        default: 'hook:updated'
      }
    },
    methods: {
      refresh: function refresh() {
        this.$forceUpdate();
      }
    },
    created: function created() {
      if (isVueComponent(this.component)) {
        this.component.$on(this.event, this.refresh);
      }
    },
    beforeDestroy: function beforeDestroy() {
      if (isVueComponent(this.component)) {
        this.component.$off(this.event, this.refresh);
      }
    },
    render: function render(createElement) {
      if (isVueComponent(this.component)) {
        return createElement(this.tag, {}, this.scoped ? this.component.$scopedSlots[this.name](this.props) : this.component.$slots[this.name]);
      }
    }
  };

  var _components;
  var TabbedMixin = {
    components: (_components = {}, _defineProperty(_components, Icon.name, Icon), _defineProperty(_components, SlotComponent.name, SlotComponent), _components),
    props: {
      value: Number,
      type: [String, Object],
      size: String,
      animated: {
        type: Boolean,
        default: true
      },
      vertical: {
        type: Boolean,
        default: false
      },
      position: String,
      destroyOnHide: {
        type: Boolean,
        default: false
      }
    },
    data: function data() {
      return {
        activeChild: this.value || 0,
        defaultSlots: [],
        contentHeight: 0,
        isTransitioning: false
      };
    },
    watch: {
      /**
       * When v-model is changed set the new active child.
       */
      value: function value(_value) {
        this.changeActive(_value);
      },

      /**
       * When child-items are updated, set active one.
       */
      childItems: function childItems() {
        var _this = this;

        if (this.activeChild < this.childItems.length) {
          var previous = this.activeChild;
          this.childItems.map(function (child, idx) {
            if (child.isActive) {
              previous = idx;

              if (previous < _this.childItems.length) {
                _this.childItems[previous].isActive = false;
              }
            }
          });
          this.childItems[this.activeChild].isActive = true;
        } else if (this.activeChild > 0) {
          this.changeActive(this.activeChild - 1);
        }
      }
    },
    methods: {
      refreshSlots: function refreshSlots() {
        this.defaultSlots = this.$slots.default || [];
      },

      /**
       * Change the active child and emit change event.
       */
      changeActive: function changeActive(newIndex) {
        if (this.activeChild === newIndex) return;
        if (newIndex > this.childItems.length) throw new Error('The index you trying to set is bigger than the childs length');

        if (this.activeChild < this.childItems.length) {
          this.childItems[this.activeChild].deactivate(this.activeChild, newIndex);
        }

        this.childItems[newIndex].activate(this.activeChild, newIndex);
        this.activeChild = newIndex;
        this.$emit('change', newIndex);
      },

      /**
      * Child click listener, emit input event and change active child.
      */
      childClick: function childClick(value) {
        if (this.activeChild === value) return;
        this.$emit('input', value);
        this.changeActive(value);
      }
    },
    mounted: function mounted() {
      if (this.activeChild < this.childItems.length) {
        this.childItems[this.activeChild].isActive = true;
      }

      this.refreshSlots();
    }
  };

  var script$1 = {
    name: 'BSteps',
    mixins: [TabbedMixin],
    props: {
      iconPack: String,
      iconPrev: {
        type: String,
        default: function _default() {
          return config.defaultIconPrev;
        }
      },
      iconNext: {
        type: String,
        default: function _default() {
          return config.defaultIconNext;
        }
      },
      hasNavigation: {
        type: Boolean,
        default: true
      },
      labelPosition: {
        type: String,
        validator: function validator(value) {
          return ['bottom', 'right', 'left'].indexOf(value) > -1;
        },
        default: 'bottom'
      },
      rounded: {
        type: Boolean,
        default: true
      },
      ariaNextLabel: String,
      ariaPreviousLabel: String
    },
    data: function data() {
      return {
        _isSteps: true // Used internally by StepItem

      };
    },
    computed: {
      wrapperClasses: function wrapperClasses() {
        return [this.size, _defineProperty({
          'is-vertical': this.vertical
        }, this.position, this.position && this.vertical)];
      },
      mainClasses: function mainClasses() {
        return [this.type, {
          'has-label-right': this.labelPosition === 'right',
          'has-label-left': this.labelPosition === 'left',
          'is-animated': this.animated,
          'is-rounded': this.rounded
        }];
      },
      childItems: function childItems() {
        return this.defaultSlots.filter(function (vnode) {
          return vnode.componentInstance && vnode.componentInstance.$data && vnode.componentInstance.$data._isStepItem;
        }).map(function (vnode) {
          return vnode.componentInstance;
        });
      },
      reversedChildItems: function reversedChildItems() {
        return this.childItems.slice().reverse();
      },

      /**
       * Check the first visible step index.
       */
      firstVisibleStepIndex: function firstVisibleStepIndex() {
        return this.childItems.map(function (step, idx) {
          return step.visible;
        }).indexOf(true);
      },

      /**
       * Check if previous button is available.
       */
      hasPrev: function hasPrev() {
        return this.firstVisibleStepIndex >= 0 && this.activeChild > this.firstVisibleStepIndex;
      },

      /**
       * Check the last visible step index.
       */
      lastVisibleStepIndex: function lastVisibleStepIndex() {
        var idx = this.reversedChildItems.map(function (step, idx) {
          return step.visible;
        }).indexOf(true);

        if (idx >= 0) {
          return this.childItems.length - 1 - idx;
        }

        return idx;
      },

      /**
       * Check if next button is available.
       */
      hasNext: function hasNext() {
        return this.lastVisibleStepIndex >= 0 && this.activeChild < this.lastVisibleStepIndex;
      },
      navigationProps: function navigationProps() {
        return {
          previous: {
            disabled: !this.hasPrev,
            action: this.prev
          },
          next: {
            disabled: !this.hasNext,
            action: this.next
          }
        };
      }
    },
    methods: {
      /**
       * Return if the step should be clickable or not.
       */
      isItemClickable: function isItemClickable(stepItem, index) {
        if (stepItem.clickable === undefined) {
          return this.activeChild > index;
        }

        return stepItem.clickable;
      },

      /**
       * Previous button click listener.
       */
      prev: function prev() {
        var _this = this;

        if (!this.hasPrev) return;
        var prevItemIdx = this.reversedChildItems.map(function (step, idx) {
          return _this.childItems.length - 1 - idx < _this.activeChild && step.visible;
        }).indexOf(true);

        if (prevItemIdx >= 0) {
          prevItemIdx = this.childItems.length - 1 - prevItemIdx;
        }

        this.$emit('input', prevItemIdx);
        this.changeActive(prevItemIdx);
      },

      /**
       * Previous button click listener.
       */
      next: function next() {
        var _this2 = this;

        if (!this.hasNext) return;
        var nextItemIdx = this.childItems.map(function (step, idx) {
          return idx > _this2.activeChild && step.visible;
        }).indexOf(true);
        this.$emit('input', nextItemIdx);
        this.changeActive(nextItemIdx);
      }
    }
  };

  /* script */
  const __vue_script__$1 = script$1;

  /* template */
  var __vue_render__$1 = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"b-steps",class:_vm.wrapperClasses},[_c('nav',{staticClass:"steps",class:_vm.mainClasses},[_c('ul',{staticClass:"step-items"},_vm._l((_vm.childItems),function(childItem,index){return _c('li',{directives:[{name:"show",rawName:"v-show",value:(childItem.visible),expression:"childItem.visible"}],key:index,staticClass:"step-item",class:[childItem.type || _vm.type, {
                      'is-active': _vm.activeChild === index,
                      'is-previous': _vm.activeChild > index
              }]},[_c('a',{staticClass:"step-link",class:{'is-clickable': _vm.isItemClickable(childItem, index)},on:{"click":function($event){_vm.isItemClickable(childItem, index) && _vm.childClick(index);}}},[_c('div',{staticClass:"step-marker"},[(childItem.icon)?_c('b-icon',{attrs:{"icon":childItem.icon,"pack":childItem.iconPack,"size":_vm.size}}):(childItem.step)?_c('span',[_vm._v(_vm._s(childItem.step))]):_vm._e()],1),_vm._v(" "),_c('div',{staticClass:"step-details"},[_c('span',{staticClass:"step-title"},[_vm._v(_vm._s(childItem.label))])])])])}),0)]),_vm._v(" "),_c('section',{staticClass:"step-content",class:{'is-transitioning': _vm.isTransitioning}},[_vm._t("default")],2),_vm._v(" "),_vm._t("navigation",[(_vm.hasNavigation)?_c('nav',{staticClass:"step-navigation"},[_c('a',{staticClass:"pagination-previous",attrs:{"role":"button","disabled":_vm.navigationProps.previous.disabled,"aria-label":_vm.ariaPreviousLabel},on:{"click":function($event){$event.preventDefault();return _vm.navigationProps.previous.action($event)}}},[_c('b-icon',{attrs:{"icon":_vm.iconPrev,"pack":_vm.iconPack,"both":"","aria-hidden":"true"}})],1),_vm._v(" "),_c('a',{staticClass:"pagination-next",attrs:{"role":"button","disabled":_vm.navigationProps.next.disabled,"aria-label":_vm.ariaNextLabel},on:{"click":function($event){$event.preventDefault();return _vm.navigationProps.next.action($event)}}},[_c('b-icon',{attrs:{"icon":_vm.iconNext,"pack":_vm.iconPack,"both":"","aria-hidden":"true"}})],1)]):_vm._e()],{"previous":_vm.navigationProps.previous,"next":_vm.navigationProps.next})],2)};
  var __vue_staticRenderFns__$1 = [];

    /* style */
    const __vue_inject_styles__$1 = undefined;
    /* scoped */
    const __vue_scope_id__$1 = undefined;
    /* module identifier */
    const __vue_module_identifier__$1 = undefined;
    /* functional template */
    const __vue_is_functional_template__$1 = false;
    /* style inject */
    
    /* style inject SSR */
    

    
    var Steps = normalizeComponent_1(
      { render: __vue_render__$1, staticRenderFns: __vue_staticRenderFns__$1 },
      __vue_inject_styles__$1,
      __vue_script__$1,
      __vue_scope_id__$1,
      __vue_is_functional_template__$1,
      __vue_module_identifier__$1,
      undefined,
      undefined
    );

  var TabbedChildMixin = {
    props: {
      label: String,
      icon: String,
      iconPack: String,
      visible: {
        type: Boolean,
        default: true
      }
    },
    data: function data() {
      return {
        isActive: false,
        transitionName: null,
        elementClass: 'item'
      };
    },
    methods: {
      /**
       * Activate element, alter animation name based on the index.
       */
      activate: function activate(oldIndex, index) {
        this.transitionName = index < oldIndex ? this.$parent.vertical ? 'slide-down' : 'slide-next' : this.$parent.vertical ? 'slide-up' : 'slide-prev';
        this.isActive = true;
      },

      /**
       * Deactivate element, alter animation name based on the index.
       */
      deactivate: function deactivate(oldIndex, index) {
        this.transitionName = index < oldIndex ? this.$parent.vertical ? 'slide-down' : 'slide-next' : this.$parent.vertical ? 'slide-up' : 'slide-prev';
        this.isActive = false;
      }
    },
    beforeDestroy: function beforeDestroy() {
      this.$parent.refreshSlots();
    },
    render: function render(createElement) {
      var _this = this;

      // if destroy apply v-if
      if (this.$parent.destroyOnHide) {
        if (!this.isActive || !this.visible) {
          return;
        }
      }

      var vnode = createElement('div', {
        directives: [{
          name: 'show',
          value: this.isActive && this.visible
        }],
        attrs: {
          'class': this.elementClass
        }
      }, this.$slots.default); // check animated prop

      if (this.$parent.animated) {
        return createElement('transition', {
          props: {
            'name': this.transitionName
          },
          on: {
            'before-enter': function beforeEnter() {
              _this.$parent.isTransitioning = true;
            },
            'after-enter': function afterEnter() {
              _this.$parent.isTransitioning = false;
            }
          }
        }, [vnode]);
      }

      return vnode;
    }
  };

  var script$2 = {
    name: 'BStepItem',
    mixins: [TabbedChildMixin],
    props: {
      step: String | Number,
      type: String | Object,
      clickable: {
        type: Boolean,
        default: undefined
      }
    },
    data: function data() {
      return {
        elementClass: 'step-item',
        _isStepItem: true // Used internally by Step

      };
    },
    created: function created() {
      if (!this.$parent.$data._isSteps) {
        this.$destroy();
        throw new Error('You should wrap bStepItem on a bSteps');
      }

      this.$parent.refreshSlots();
    }
  };

  /* script */
  const __vue_script__$2 = script$2;

  /* template */

    /* style */
    const __vue_inject_styles__$2 = undefined;
    /* scoped */
    const __vue_scope_id__$2 = undefined;
    /* module identifier */
    const __vue_module_identifier__$2 = undefined;
    /* functional template */
    const __vue_is_functional_template__$2 = undefined;
    /* style inject */
    
    /* style inject SSR */
    

    
    var StepItem = normalizeComponent_1(
      {},
      __vue_inject_styles__$2,
      __vue_script__$2,
      __vue_scope_id__$2,
      __vue_is_functional_template__$2,
      __vue_module_identifier__$2,
      undefined,
      undefined
    );

  var use = function use(plugin) {
    if (typeof window !== 'undefined' && window.Vue) {
      window.Vue.use(plugin);
    }
  };
  var registerComponent = function registerComponent(Vue, component) {
    Vue.component(component.name, component);
  };

  var Plugin = {
    install: function install(Vue) {
      registerComponent(Vue, Steps);
      registerComponent(Vue, StepItem);
    }
  };
  use(Plugin);

  exports.BStepItem = StepItem;
  exports.BSteps = Steps;
  exports.default = Plugin;

  Object.defineProperty(exports, '__esModule', { value: true });

}));
