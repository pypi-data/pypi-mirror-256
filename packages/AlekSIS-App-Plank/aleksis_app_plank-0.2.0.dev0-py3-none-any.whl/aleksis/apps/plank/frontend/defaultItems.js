export default {
  inventory: { name: "", checkOutCreateGroup: null, checkOutGroups: [] },
  category: {
    name: "",
    notes: "",
    inventory: null,
    colour: "#00000000",
    icon: "",
  },
  manufacturer: { name: "", notes: "", inventory: null },
  location: { name: "", notes: "", parent: null, inventory: null },
  itemType: {
    name: "",
    description: "",
    partNumber: "",
    image: "",
    manufacturer: null,
    category: null,
  },
  item: {
    barcode: "",
    name: "",
    notes: "",
    category: null,
    itemType: null,
    location: null,
    serialNumber: "",
  },
  checkOutProcess: {
    checkInUntil: null,
    condition: null,
  },
};
