export default {
  meta: {
    inMenu: true,
    titleKey: "plank.menu_title",
    icon: "mdi-warehouse",
    permission: "plank.view_menu_rule",
  },
  children: [
    {
      path: "inventories/",
      component: () => import("./components/inventory/InventoryList.vue"),
      name: "plank.inventories",
      meta: {
        inMenu: true,
        titleKey: "plank.inventory.menu_title",
        icon: "mdi-folder-home-outline",
        permission: "plank.view_inventories_rule",
      },
    },
    {
      path: "inventories/:pk/",
      component: () => import("./components/inventory/InventoryDetail.vue"),
      name: "plank.inventory",
    },
    {
      path: "categories/",
      component: () => import("./components/category/CategoryList.vue"),
      name: "plank.categories",
      meta: {
        inMenu: true,
        titleKey: "plank.category.menu_title",
        icon: "mdi-label-multiple-outline",
        permission: "plank.view_categories_rule",
      },
    },
    {
      path: "manufacturers/",
      component: () => import("./components/manufacturer/ManufacturerList.vue"),
      name: "plank.manufacturers",
      meta: {
        inMenu: true,
        titleKey: "plank.manufacturer.menu_title",
        icon: "mdi-factory",
        permission: "plank.view_manufacturers_rule",
      },
    },
    {
      path: "manufacturers/:pk/",
      component: () =>
        import("./components/manufacturer/ManufacturerDetail.vue"),
      name: "plank.manufacturer",
    },
    {
      path: "locations/",
      component: () => import("./components/location/LocationList.vue"),
      name: "plank.locations",
      meta: {
        inMenu: true,
        titleKey: "plank.location.menu_title",
        icon: "mdi-map-marker-multiple-outline",
        permission: "plank.view_locations_rule",
      },
    },
    {
      path: "locations/:pk/",
      component: () => import("./components/location/LocationDetail.vue"),
      name: "plank.location",
    },
    {
      path: "locations/:pk/completeness/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "plank.locationCompleteness",
    },
    {
      path: "item_types/",
      component: () => import("./components/item_type/ItemTypeList.vue"),
      name: "plank.itemTypes",
      meta: {
        inMenu: true,
        titleKey: "plank.item_type.menu_title",
        icon: "mdi-shape-outline",
        permission: "plank.view_itemtypes_rule",
      },
    },
    {
      path: "item_types/:pk/",
      component: () => import("./components/item_type/ItemTypeDetail.vue"),
      name: "plank.itemType",
    },
    {
      path: "items/",
      component: () => import("./components/item/PlankItemList.vue"),
      name: "plank.items",
      meta: {
        inMenu: true,
        titleKey: "plank.item.menu_title",
        icon: "mdi-inbox-multiple-outline",
        permission: "plank.view_items_rule",
      },
    },
    {
      path: "items/:pk/",
      component: () => import("./components/item/ItemDetail.vue"),
      name: "plank.item",
    },
    {
      path: "inventory/",
      component: () =>
        import("./components/inventory_process/InventoryForm.vue"),
      name: "plank.inventoryForm",
      meta: {
        inMenu: true,
        titleKey: "plank.item.inventory_process.menu_title",
        icon: "mdi-import",
        permission: "plank.create_item_rule",
      },
    },
    {
      path: "checks/out/",
      component: () => import("./components/check_out/CheckOutPage.vue"),
      name: "plank.checkOut",
      meta: {
        inMenu: true,
        titleKey: "plank.check_out.menu_title",
        icon: "mdi-cart-arrow-down",
        permission: "plank.check_out_rule",
      },
    },
    {
      path: "checks/:pk/check-out-form.pdf",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "plank.checkOutForm",
    },
    {
      path: "checks/",
      component: () =>
        import("./components/check_out_process/CheckOutProcessList.vue"),
      name: "plank.checkOutProcesses",
      meta: {
        inMenu: true,
        titleKey: "plank.check_out_process.menu_title",
        icon: "mdi-cart-outline",
        permission: "plank.view_checkoutprocesses_rule",
      },
    },
    {
      path: "checks/:pk/",
      component: () =>
        import("./components/check_out_process/CheckOutProcessDetail.vue"),
      name: "plank.checkOutProcess",
    },
    {
      path: "checks/:pk/check-in-form.pdf",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "plank.checkInForm",
    },
    {
      path: "checks/in/",
      component: () => import("./components/check_in/CheckInPage.vue"),
      name: "plank.checkIn",
      meta: {
        inMenu: true,
        titleKey: "plank.check_in.menu_title",
        icon: "mdi-cart-arrow-up",
        permission: "plank.check_in_rule",
      },
    },
  ],
};
