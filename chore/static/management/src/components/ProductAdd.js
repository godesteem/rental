import React, {useEffect, useState} from 'react';
import API from '../lib/api';
import myTheme from '../lib/theme';
import Paper from "@material-ui/core/Paper";
import FormGroup from '@material-ui/core/FormGroup';
import makeStyles from "@material-ui/core/styles/makeStyles";
import TextField from "@material-ui/core/TextField";
import FormControl from "@material-ui/core/FormControl";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import Button from "@material-ui/core/Button";
import Input from "@material-ui/core/Input";
import Fab from "@material-ui/core/Fab";
import Tab from "@material-ui/core/Tab";
import Tabs from "@material-ui/core/Tabs";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import AddIcon from "@material-ui/icons/Add";
import ProductDetail from "./ProductDetail";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      <Box p={3}>{children}</Box>
    </Typography>
  );
}
function a11yProps(index) {
  return {
    id: `tab-${index}`,
    'aria-controls': `tabpanel-${index}`,
  };
}
const formControl = (theme) => ({
  margin: theme.spacing(1),
  minWidth: 120,
  width: '100%',
});
const useStyles = makeStyles(theme => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  tableHead: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  whiteText: {
    color: theme.palette.common.white,
  },
  darkRow: {
    backgroundColor: '#6e6e6e',
  },
  lightRow: {
    backgroundColor: '#ccc',
  },
  fab:{
    float: 'right',
    marginTop: '0.75rem',
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
  formGroup: {
    display: 'flex',
    marginTop: '1rem',
  },
  formControl: formControl(theme),
  formControl50: {
    ...formControl(theme),
    width: '50%',
  },
  formControl30: {
    ...formControl(theme),
    width: '30%',
  },
  rootPaper: {
    maxWidth: '40%',
    margin: 'auto',
    padding: '0.5rem',
  },
  submitButton: {
    backgroundColor: theme.palette.success,
  },
  chip: {
    margin: 2,
  },
  priceLabel: {
    zIndex: 200,
    background: theme.palette.common.white,
    padding: '0 0.5rem',
  }
}));
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};
export default function ProductAdd(props) {
  const classes = useStyles(myTheme);
  const isEdit = !!props.match.params.id;
  const productId = props.match.params.id || undefined;
  const [currentStep, setStep] = useState( 0);
  const [product, setProduct] = useState(undefined);
  const [name, setName] = useState(product ? product.name : '');
  const [price, setPrice] = useState(product ? product.price : undefined);
  const [currency, setCurrency] = useState(product ? product.currency : 'EUR');
  const [components, setComponents] = useState([]);
  const [allComponents, setAllComponents] = useState([]);
  const [finishedProduct, setFinishedProduct] = useState(undefined);
  useEffect(() => {
    async function getComponents(){
      if(currentStep === 1){
        const result = await API.get('warehouse-components/');
        if(result){
          setAllComponents(result.data);
        }
      }
    }
    getComponents()
  }, [currentStep])
  useEffect( () => {
    async function getData(){
      if(isEdit) {
        const result = await API.get(`products/${productId}/`);
        if (result) {
          setProduct(result.data);
          let newComponents = []
          if(result.data.components)
            newComponents = result.data.components.map((elem, id)=>{
              return {id, component_id: elem.component.id, quantity: elem.quantity}
            })
            setComponents(newComponents)
          setPrice(result.data.price);
          setName(result.data.name);
          setCurrency(result.data.currency);
          setFinishedProduct({product: result.data, warehouse_components: result.data.components ? result.data.components.map((elem) => {
            return {component: {name: elem.component.name}, quantity: elem.quantity}
            }): []})
        }
      }
    }
    getData()
    }, [isEdit, productId]);
  function updateComponents(component){
    const componentsCopy = components;
    if(!component.quantity && !component.component_id)
      componentsCopy.push(component);
    const newComponents = componentsCopy.map((elem) => {
      if(elem.id === component.id)
        elem = component;
      return elem
    });
    setComponents(newComponents);
  }
  async function submitStep(targetStep){
    async function postProduct(){
      if(isEdit){
        return await API.put(`products/${productId}/`, {name, price, currency}).catch((e) => console.log(e))
      }
      else {
        return await API.post(`products/`, {name, price, currency}).catch((e) => console.log(e))
      }
    }
    async function postComponents(){
      if(isEdit) {
        return await API.patch(`warehouse-items/${productId}/`, {
          warehouse_components_list: components.map(elem => ({
            component_id: elem.component_id,
            quantity: elem.quantity
          }))
        }).catch((e) => console.log(e))
      }
      else{
        return await API.post('warehouse-items/', {
          product_id: productId,
          warehouse_components_list: components.map(elem => ({
            component_id: elem.component_id,
            quantity: elem.quantity
          }))
        }).catch((e) => console.log(e))
      }
    }
    if(currentStep === 0) {
      const response = await postProduct();
      if(!!response){
        setProduct(response.data)
      }
    }
    else if(currentStep === 1){
      const response = await postComponents();
      if(!!response){
        setFinishedProduct(response.data);
      }
    }
    setStep(targetStep);
  }
  return (
    <div>
      <h1 className={classes.title}>{finishedProduct ? `Name: ${finishedProduct.product.name}` : `${isEdit ? 'Edit' : 'Add'} Product`}</h1>
      <Paper className={classes.rootPaper}>
        <FormGroup className={classes.formGroup} onSubmit={() => submitStep()}>
          <Tabs value={currentStep} onChange={(e, step) => setStep(step)} aria-label="Label">
            <Tab label="Product" {...a11yProps(0)} />
            <Tab label="Components" {...a11yProps(1)} />
            <Tab label="Overview" {...a11yProps(2)}/>
          </Tabs>
          <TabPanel value={currentStep} index={0}>
            <FormControl variant="filled" className={classes.formControl}>
              <TextField
                label="Name"
                variant="outlined"
                color="secondary"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </FormControl>
            <div>
              <FormControl variant="filled" className={classes.formControl50} style={{float: 'left'}}>
                <InputLabel variant={'outlined'} id={'price-label'} className={classes.priceLabel} shrink={!!price} htmlFor="price">
                  Price
                </InputLabel>
                <TextField
                  labelid={'price-label'}
                  variant="outlined"
                  color="secondary"
                  id={'price'}
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}/>
              </FormControl>
              <FormControl variant="filled" className={classes.formControl} style={{float: 'right', width: '40%'}}>
                <Select
                  labelid="select-currency-label"
                  id="select-currency"
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                >
                  <MenuItem value={'EUR'}>€</MenuItem>
                  <MenuItem value={'USD'}>$</MenuItem>
                </Select>
                <InputLabel id="select-currency-label">Currency</InputLabel>
              </FormControl>
            </div>
            <FormControl variant="filled" className={classes.formControl} style={{display: 'inline-block'}}>
              <Button
                onClick={() => submitStep(0)}
                fullWidth={!isEdit}
                type="submit"
                variant="contained"
                color="primary"
                style={{width: isEdit ? '50%' : '100%'}}
                className={classes.submitButton}>
                Update
              </Button>
              <Button
                onClick={() => submitStep(1)}
                fullWidth={!isEdit}
                style={{width: isEdit ? '50%' : '100%'}}
                size={isEdit ? 'medium' : 'large'}
                type="submit"
                variant="contained"
                color="primary"
                className={classes.submitButton}>
                Next
              </Button>
            </FormControl>
          </TabPanel>
          <TabPanel value={currentStep} index={1}>
          <div style={{display: 'inline'}}>{components.map((elem, groupId) => {
          return (<div key={groupId}><FormControl variant="filled" className={classes.formControl50}>
              <InputLabel id={`select-components-label-${groupId}`}>Component</InputLabel>
              <Select
                labelId={`select-components-label-${groupId}`}
                id={`select-components-${groupId}`}
                value={elem.component_id}
                InputLabelProps={isEdit ? {
                  shrink: isEdit,
                } : {}}
                onChange={(e) => updateComponents({id: elem.id, component_id:  e.target.value, quantity: elem.quantity})}
              >
                {allComponents && allComponents.map((elem, id) => {
                  return (<MenuItem key={`${elem.id}-${groupId}`} value={elem.id}>{elem.name}</MenuItem>)
                })}
              </Select>
            </FormControl>
            <FormControl variant="filled" className={classes.formControl30}>
              <InputLabel id={`quantity-${groupId}-label`}>Quantity</InputLabel>
              <Input type={'number'} id={`quantity-${groupId}`} labelId={`quantity-${groupId}-label`}
                     value={elem.quantity}
              onChange={(e) => updateComponents({id: elem.id, component_id:  elem.component_id, quantity: Number(e.target.value)})}/>
            </FormControl>
          </div>)})}
          <Fab color="primary" aria-label="add" className={classes.fab} onClick={() => updateComponents({id: components.length + 1, component_id:  null, quantity: null})}>
            <AddIcon />
          </Fab>
        </div>

          <FormControl variant="filled" className={classes.formControl} style={{display: 'inline-block'}}>
            <Button
              onClick={() => submitStep(1)}
              fullWidth={!isEdit}
              type="submit"
              variant="contained"
              color="primary"
              style={{width: isEdit ? '50%' : '100%'}}
              className={classes.submitButton}>
              Update
            </Button>
            <Button
              onClick={() => submitStep(2)}
              fullWidth={!isEdit}
              style={{width: isEdit ? '50%' : '100%'}}
              size={isEdit ? 'medium' : 'large'}
              type="submit"
              variant="contained"
              color="primary"
              className={classes.submitButton}>
              Next
            </Button>
          </FormControl>

          </TabPanel>
        </FormGroup>
        <TabPanel value={currentStep} index={2}>
          {currentStep === 2 && finishedProduct ? (<ProductDetail data={finishedProduct}/>) : null}
        </TabPanel>
      </Paper>
    </div>
  )
}