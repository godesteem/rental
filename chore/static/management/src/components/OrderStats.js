import React, {useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import rentalAPI from "../lib/api";
import {getCookie} from '../lib/cookies';

const useStyles = makeStyles({
  card: {
    minWidth: 275,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

const API = new rentalAPI({token: getCookie('JWT')});

export default function OrderStats(props) {
  const classes = useStyles();
  const [orders, setOrders] = useState([]);
  useEffect( () => {
    async function getData(){
      const result = await API.getOrders();
      if(result)
        setOrders(result.data);
    }
    getData()
    }, []);
  return (
    <Card className={classes.card}>
      <CardContent>

      </CardContent>
      <CardActions>
        <Button size="small">Show</Button>
      </CardActions>
    </Card>
  )
}