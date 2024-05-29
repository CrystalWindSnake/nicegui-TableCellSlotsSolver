export default {
  template: `<div><slot></slot></div>`,
  props: {
    id: String,
    props: Object,
  },
  async mounted() {
    if (this.id === null) {
      return;
    }
    await this.$nextTick()
    const target = getElement(this.id);
    runMethod(target, 'notify', [this.props])
  },
};