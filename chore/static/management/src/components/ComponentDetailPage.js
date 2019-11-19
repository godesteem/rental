import React, {useEffect, useState} from "react";
import rentalAPI from "../lib/api";
import {getCookie} from "../lib/cookies";
import ProductDetail from "./ProductDetail";
import Paper from "@material-ui/core/Paper";
import myTheme from "../lib/theme";
import makeStyles from "@material-ui/core/styles/makeStyles";
import Fab from "@material-ui/core/Fab";
import EditIcon from "@material-ui/icons/Edit";
import ComponentDetail from "./ComponentDetail";

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
const API = new rentalAPI({token: getCookie("JWT")});
export default function ComponentDetailPage(props) {
  const classes = useStyles(myTheme);
  const [componentId, setComponentId] = useState(props.match.params.id || undefined)
  const [component, setComponent] = useState(props.data || undefined)
  useEffect( () => {
    async function getData(){
      const result = await API.getWarehouseComponent(componentId);
      if(result)
        setComponent(result.data);
    }
    getData()
    }, [componentId]);
  if(!component)
    return null
  return (

    <div>
      <h1 className={classes.title}>{component ? `Name: ${component.name}` : ``}</h1>
      <Paper className={classes.rootPaper}>
        <ComponentDetail data={component}/>
      </Paper>
      <Fab color="primary" aria-label="add" className={classes.fab} onClick={() => window.location.replace(`/management/components/${component.id}/edit`)}>
        <EditIcon />
      </Fab>
    </div>
  )
}