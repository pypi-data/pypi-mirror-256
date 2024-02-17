export default {
  component: () => import("aleksis.core/components/Parent.vue"),
  meta: {
    inMenu: true,
    titleKey: "buelleten.menu_title",
    icon: "mdi-monitor",
    permission: "buelleten.view_menu_rule",
  },
  children: [
    {
      path: "display_groups/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.displayGroups",
      meta: {
        inMenu: true,
        titleKey: "buelleten.display_groups.menu_title",
        icon: "mdi-monitor-multiple",
        permission: "buelleten.view_display_groups_rule",
      },
    },
    {
      path: "display_groups/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.createDisplayGroup",
    },
    {
      path: "display_groups/:pk/edit",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.editDisplayGroup",
    },
    {
      path: "display_groups/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.displayGroupById",
    },
    {
      path: "api/impressive/:slug.txt",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.impressiveDisplayList",
    },
    {
      path: "displays/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.displays",
    },
    {
      path: "displays/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.createDisplay",
    },
    {
      path: "displays/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.editDisplay",
    },
    {
      path: "slides/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.editSlide",
    },
    {
      path: "slides/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.deleteSlide",
    },
    {
      path: "slides/:app/:model/new/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
      name: "buelleten.createSlide",
    },
  ],
};
