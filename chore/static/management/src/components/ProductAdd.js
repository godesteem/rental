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
  },
  root: {
    display: 'flex',
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  rootPaper: {
    maxWidth: '40%',
    margin: 'auto',
    padding: '0.5rem',
  },
  submitButton: {
    backgroundColor: theme.palette.success
  }
}));

export default function ProductAdd(props) {
  const classes = useStyles(myTheme);
  const [currentStep, setStep] = useState(1);
  const [name, setName] = useState(undefined);
  const [price, setPrice] = useState(undefined);
  const [currency, setCurrency] = useState('EUR');
  const [product, setProduct] = useState(undefined);
  useEffect( () => {
    // async function getData(){
    //   const result = await API.get('products/');
    //   if(result)
    //     setProducts(result.data);
    // }
    // getData()
    }, []);
  function submitStep(){
    console.log('CALL')
    async function postProduct(){
      return await API.post('products/', {name, price, currency}).catch((e) => console.log(e))
    }
    if(currentStep === 1) {
      const response = postProduct()
      if(response){
        setProduct(response.data)
        setStep(2)
      }
    }
  }
  return (
    <div>
      <h1 className={classes.title}>Add Product</h1>
      <Paper className={classes.rootPaper}>
        {currentStep === 1 && (<><FormGroup className={classes.root} onSubmit={() => submitStep()}>
          <TextField
            id="outlined-secondary"
            label="Name"
            variant="outlined"
            color="secondary"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </FormGroup>
        <FormGroup>
          <TextField
            id="outlined-secondary"
            label="Price"
            variant="outlined"
            color="secondary"
            value={price}
            helperText={"In Cents!"}
            onChange={(e) => setPrice(e.target.value)}
          />
          <FormControl variant="filled" className={classes.formControl}>
            <InputLabel id="select-currency-label">Currency</InputLabel>
            <Select
              labelId="select-currency-label"
              id="select-currency"
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
            >
              <MenuItem value={'EUR'}>€</MenuItem>
              <MenuItem value={'USD'}>$</MenuItem>
            </Select>
          </FormControl>
          <Button onClick={() => submitStep()} type="submit" variant="contained" color="primary" className={classes.submitButton}>Next</Button>
        </FormGroup></>)}
        {currentStep === 2 && (<FormGroup>

          </FormGroup>)}
      </Paper>
    </div>
  )
}