import React, {useEffect, useState} from 'react';
import rentalAPI from '../lib/api';
import {getCookie} from "../lib/cookies";
import myTheme from '../lib/theme';
import Paper from "@material-ui/core/Paper";
import FormGroup from '@material-ui/core/FormGroup';
import makeStyles from "@material-ui/core/styles/makeStyles";
import TextField from "@material-ui/core/TextField";
import FormControl from "@material-ui/core/FormControl";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import Input from "@material-ui/core/Input";
import Fab from "@material-ui/core/Fab";
import Tab from "@material-ui/core/Tab";
import Tabs from "@material-ui/core/Tabs";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import AddIcon from "@material-ui/icons/Add";
import UpdateNextButtons from "./UpdateNextButtons";
import {Link} from "react-router-dom";
import ComponentDetail from "./ComponentDetail";

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
    width: '50%',
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
const API = new rentalAPI({token: getCookie("JWT")});
export default function ComponentAdd(props) {
  const classes = useStyles(myTheme);
  const isEdit = !!props.match.params.id;
  const componentId = props.match.params.id || undefined;
  const [currentStep, setStep] = useState( 0);
  const [component, setComponent] = useState(undefined);
  const [name, setName] = useState(component ? component.name : '');
  const [storageUnits, setStorageUnits] = useState([]);
  const [allStorageUnits, setAllStorageUnits] = useState([]);
  const [finishedComponent, setFinishedComponent] = useState(undefined);
  useEffect(() => {
    async function getStorageUnits(){
      if(currentStep === 1){
        const result = await API.getStorageUnits();
        if(result){
          setAllStorageUnits(result.data);
        }
      }
    }
    getStorageUnits()
  }, [currentStep])
  useEffect( () => {
    async function getData(){
      if(isEdit) {
        const result = await API.getWarehouseComponent(componentId);
        if (result) {
          setComponent(result.data);
          let newStorageUnits = []
          if(result.data.storage_units)
            newStorageUnits = result.data.storage_units.map((elem, id)=>{
              return {id, storage_unit_id: elem.id, name: elem.storage_unit.name, quantity: elem.quantity}
            })
            setStorageUnits(newStorageUnits)
          setName(result.data.name);
          setFinishedComponent({id: result.data.id, name: result.data.name, storage_units: newStorageUnits})
        }
      }
    }
    getData()
    }, [isEdit, componentId]);
  function updateStorageUnits(storageUnit){
    const storageUnitCopy = storageUnits;
    if(!storageUnit.quantity && !storageUnit.storage_unit_id)
      storageUnitCopy.push(storageUnit);
    const newStorageUnits = storageUnitCopy.map((elem) => {
      if(elem.id === storageUnit.id)
        elem = storageUnit;
      return elem
    });
    setStorageUnits(newStorageUnits);
  }
  async function submitStep(targetStep, skip){
    if(skip) {
      setStep(targetStep);
      return;
    }

    if(currentStep === 0) {
      const response = await API.postComponent(isEdit, componentId, {name});
      if(!!response){
        setComponent(response.data)
        if(!isEdit){
          window.location.replace(`/management/components/${response.data.id}/edit`)
        }
      }
    }
    else if(currentStep === 1 && !isEdit){
      const response = await API.postComponent(isEdit, componentId, {name, storageUnits});
      if(!!response){
        setFinishedComponent(response.data);
      }
    }
    setStep(targetStep);
  }
  return (
    <div>
      <h1 className={classes.title}>{finishedComponent ? `Name: ${finishedComponent.name}` : `${isEdit ? 'Edit' : 'Add'} Component`}</h1>
      <Paper className={classes.rootPaper}>
        <FormGroup className={classes.formGroup} onSubmit={() => submitStep()}>
          <Tabs value={currentStep} onChange={(e, step) => setStep(step)} aria-label="Label">
            <Tab label="Component" {...a11yProps(0)} />
            <Tab label="Storage Units" {...a11yProps(1)} />
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
            <FormControl variant="filled" className={classes.formControl} style={{display: 'inline-block'}}>
              <UpdateNextButtons isEdit={isEdit} currentStep={0} submitStep={submitStep.bind(this)}/>
            </FormControl>
          </TabPanel>
          <TabPanel value={currentStep} index={1}>
            <Link to={'/management/components'}>Edit Components</Link>
          <div style={{display: 'inline'}}>{storageUnits.map((elem, groupId) => {
          return (<div key={groupId}><FormControl variant="filled" className={classes.formControl50}>
              <InputLabel id={`select-storage-units-label-${groupId}`}>Storage Unit</InputLabel>
              <Select
                labelId={`select-storage-units-label-${groupId}`}
                id={`select-storage-units-${groupId}`}
                value={!!allStorageUnits ? elem.storage_unit_id : ''}
                InputLabelProps={isEdit ? {
                  shrink: isEdit,
                } : {}}
                onChange={(e) => updateStorageUnits({id: elem.id, storage_unit_id:  e.target.value, quantity: elem.quantity})}
              >
                {allStorageUnits && allStorageUnits.map((elem, id) => {
                  return (<MenuItem key={`${id}-${groupId}`} value={elem.id}>{elem.name}</MenuItem>)
                })}
              </Select>
            </FormControl>
            <FormControl variant="filled" className={classes.formControl30}>
              <InputLabel id={`quantity-${groupId}-label`}>Quantity</InputLabel>
              <Input type={'number'} id={`quantity-${groupId}`} labelId={`quantity-${groupId}-label`}
                     value={elem.quantity}
              onChange={(e) => updateStorageUnits({id: groupId, storage_unit_id:  elem.storage_unit_id, quantity: Number(e.target.value)})}/>
            </FormControl>
          </div>)})}
          <Fab color="primary" aria-label="add" className={classes.fab} onClick={() => updateStorageUnits({id: storageUnits.length + 1, storage_unit_id:  null, quantity: null})}>
            <AddIcon />
          </Fab>
        </div>

          <FormControl variant="filled" className={classes.formControl} style={{display: 'inline-block'}}>
            <UpdateNextButtons isEdit={isEdit} currentStep={1} submitStep={submitStep.bind(this)}/>
          </FormControl>

          </TabPanel>
        </FormGroup>
        <TabPanel value={currentStep} index={2}>
          {currentStep === 2 && finishedComponent ? (<ComponentDetail data={finishedComponent}/>) : null}
        </TabPanel>
      </Paper>
    </div>
  )
}