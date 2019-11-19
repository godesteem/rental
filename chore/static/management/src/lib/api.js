import axios from 'axios';

const api = axios.create({
  baseURL: `http://localhost:8000/api/`,
  defaults: {
    xsrfHeaderName: 'X-CSRFTOKEN',
    xsrfCookieName: 'csrftoken',
  },
  headers: {
    // accessControlAllowOrigin: '*',
    // accessControlAllowCredentials: 'true',
    // accessControlAllowMethods: 'GET,HEAD,OPTIONS,POST,PUT,PATCH',
    // accessControlAllowHeaders: 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers',
  }
});


export default class rentalAPI {
  constructor(props) {
    this.token = props.token;
    this.config = {headers: {'Authorization': `JWT ${this.token}`}};
  };

  async postNestedComponents(isEdit, productId, components) {
    if (isEdit) {
      return await api.patch(`warehouse-items/${productId}/`, {
        warehouse_components_list: components.map(elem => ({
          component_id: elem.component_id,
          quantity: elem.quantity
        }))
      }, this.config).catch((e) => console.log(e))
    } else {
      return await api.post('warehouse-items/', {
        product_id: productId,
        warehouse_components_list: components.map(elem => ({
          component_id: elem.component_id,
          quantity: elem.quantity
        }))
      }, this.config).catch((e) => console.log(e))
    }
  }
  async postComponent(isEdit, componentId, {name, storageUnits}){
    if(isEdit){
      return await api.put(`warehouse-components/${componentId}/`, {
        name,
        storage_units: storageUnits
      }, this.config).catch((e) => console.log(e));
    }
    else{
      return await api.post(`warehouse-components/`, {
        name,
        storage_units: storageUnits
      }, this.config).catch((e) => console.log(e))
    }
  }

  async postProduct(isEdit, productId, {name, price, currency}) {
    if (isEdit) {
      return await api.put(`products/${productId}/`, {name, price, currency}, this.config).catch((e) => console.log(e))
    } else {
      return await api.post(`products/`, {name, price, currency}, this.config).catch((e) => console.log(e))
    }
  }

  async getProducts() {
    return await api.get('products/', this.config);
  }

  async getProduct(productId) {
    return await api.get(`products/${productId}/`, this.config)
  }

  async getWarehouseComponents() {
    return await api.get('warehouse-components/', this.config);
  }
  async getWarehouseComponent(componentId) {
    return await api.get(`warehouse-components/${componentId}/`, this.config);
  }
  async getStorageUnits(){
    return await api.get('storage-units/', this.config);
  }

  getOrders = async () => {
    return await api.get('orders/', this.config);
  }

  getToken = async (username, password) => {
    return await api.post('token/', {username, password})
  }
}