import React, {useEffect, useState} from 'react';
import rentalAPI from "../lib/api";
import {getCookie} from "../lib/cookies";
import Fab from "@material-ui/core/Fab";
import AddIcon from "@material-ui/icons/Add";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import {TableBody} from "@material-ui/core";
import {Link} from "react-router-dom";
import makeStyles from "@material-ui/core/styles/makeStyles";

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
    float: 'left',
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
}));


const API = new rentalAPI({token: getCookie("JWT")});
export default function ComponentsList(props) {
  const classes = useStyles();
  const [components, setComponents] = useState([]);
  useEffect(() => {
    async function getComponents(){
      const result = await API.getWarehouseComponents();
      if(result){
        setComponents(result.data);
      }
    }
    getComponents()
  }, [])
  if(!components)
    return null;

  return (
    <div>
      <h1 className={classes.title}>Components</h1>
      <Fab color="primary" aria-label="add" className={classes.fab} onClick={() => window.location.replace('/management/components/add')}>
        <AddIcon />
      </Fab>
      <Paper>
        <Table>
          <TableHead className={classes.tableHead}>
            <TableRow>
              <TableCell><b className={classes.whiteText}>ID</b></TableCell>
              <TableCell><b className={classes.whiteText}>Name</b></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
      {components.map((component, id) => {
        return(<TableRow key={id} className={id % 2 ? classes.darkRow : classes.lightRow}>
            <TableCell><Link to={`/management/components/${component.id}/detail`}>{component.id}</Link></TableCell>
            <TableCell>{component.name}</TableCell>
          </TableRow>
        )
      })}
          </TableBody>
        </Table>
      </Paper>
    </div>
  )
}