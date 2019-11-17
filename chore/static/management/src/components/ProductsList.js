import React, {useEffect, useState} from 'react';
import API from '../lib/api';
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Fab from "@material-ui/core/Fab";
import AddIcon from '@material-ui/icons/Add';
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

export default function ProductsList(props) {
  const classes = useStyles();
  const [products, setProducts] = useState([]);
  useEffect( () => {
    async function getData(){
      const result = await API.get('products/');
      if(result)
        setProducts(result.data);
    }
    getData()
    }, []);
  return (
    <div>
      <h1 className={classes.title}>Products</h1>
      <Fab color="primary" aria-label="add" className={classes.fab} onClick={() => window.location.replace('/management/products/add')}>
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
      {products.map((product, id) => {
        return(<TableRow key={id} className={id % 2 ? classes.darkRow : classes.lightRow}>
            <TableCell>{product.id}</TableCell>
            <TableCell>{product.name}</TableCell>
          </TableRow>
        )
      })}
        </Table>
      </Paper>
    </div>
  )
}