<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="location"
    item-attribute="name"
    :default-item="defaultItem"
    :show-create="formData.canCreate"
    v-bind="$attrs"
  >
    <template
      v-for="(_, name) in $scopedSlots"
      :slot="name"
      slot-scope="slotData"
    >
      <slot :name="name" v-bind="slotData" />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.name="{ item }">
      <router-link :to="{ name: 'plank.location', params: { id: item.id } }">
        {{ item.name }}
      </router-link>
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.breadcrumbs="{ item }">
      <v-breadcrumbs
        :items="
          item.breadcrumbs.slice(0, -1).map((t) => {
            return { text: t };
          })
        "
        class="pa-0"
      ></v-breadcrumbs>
    </template>
    <template #fields="{ currentItem }">
      <inventory-input
        :inventories="formData.inventories"
        v-model="currentItem.inventory"
      />
      <location-input
        v-model="currentItem.parent"
        :locations="formData.locations"
        v-if="'parent' in currentItem"
      />
      <name-input v-model="currentItem.name" />
      <notes-input v-model="currentItem.notes" />
    </template>
  </item-list>
</template>

<script>
import rules from "../../rules";
import ItemList from "../ItemList.vue";
import defaultItems from "../../defaultItems";
import InventoryInput from "../inputs/InventoryInput.vue";
import NameInput from "../inputs/NameInput.vue";
import NotesInput from "../inputs/NotesInput.vue";
import LocationInput from "../inputs/LocationInput.vue";
import gqlFormData from "./formData.graphql";
export default {
  name: "LocationBaseList",
  components: {
    NotesInput,
    NameInput,
    InventoryInput,
    ItemList,
    LocationInput,
  },
  apollo: {
    formData: {
      query: gqlFormData,
      result({ data }) {
        if (data) {
          this.formData = data;
        }
      },
    },
  },
  computed: {
    headers() {
      return [
        {
          text: this.$t("plank.labels.id"),
          value: "id",
        },
        {
          text: this.$t("plank.inventory.title"),
          value: "inventory.name",
        },
        {
          text: this.$t("plank.location.parents"),
          value: "breadcrumbs",
        },
        {
          text: this.$t("plank.item.title_plural"),
          value: "itemsCount",
        },
        { text: this.$t("plank.labels.name"), value: "name" },
      ];
    },
  },
  data() {
    return {
      defaultItem: defaultItems.location,
      rules: rules,
      formData: {
        inventories: [],
        locations: [],
        canCreate: false,
      },
    };
  },
};
</script>
