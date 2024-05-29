
export default {
  template: `<slot></slot>`,
  data() {
    this.notifyTasks = [];
    this.loaded = false;
  },

  methods: {
    notify(props) {
      if (!this.loaded) {
        this.notifyTasks.push(props);
      } else {
        this.$emit("notify", props);
      }
    },

    triggerNotifyTasks() {
      this.notifyTasks.forEach(props => {
        this.$emit("notify", props);
      })
      this.notifyTasks.length = 0;
    },

    setLoaded() {
      this.loaded = true;
    }

  }
};