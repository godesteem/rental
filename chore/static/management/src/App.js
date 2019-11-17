import React from 'react';
import Button from '@material-ui/core/Button';
import {Container} from "@material-ui/core";
import {AppBar} from "@material-ui/core";
import {Toolbar} from "@material-ui/core";
import {IconButton} from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";
import {Typography} from "@material-ui/core";
import makeStyles from "@material-ui/core/styles/makeStyles";
import {ThemeProvider} from "@material-ui/core/styles";
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom';
import ProductsList from "./components/ProductsList";
import ProductAdd from "./components/ProductAdd";
import theme from './lib/theme';

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));
function App() {
  const classes = useStyles();
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Container>
          <AppBar position="static">
            <Toolbar>
              <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" className={classes.title}>
                <Link to="/management/products">Products</Link>
              </Typography>
              <Button color="inherit">Login</Button>
            </Toolbar>
          </AppBar>
        </Container>
        <Container>
            <Switch>
              <Route exact path="/management/products" component={ProductsList}/>
              <Route exact path="/management/products/add" component={ProductAdd}/>
            </Switch>
        </Container>
      </Router>
    </ThemeProvider>

    );
}

export default App;
