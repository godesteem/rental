import React, {useState} from 'react';
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
import ProductDetailPage from "./components/ProductDetailPage";
import Overview from "./components/Overview";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogActions from "@material-ui/core/DialogActions";
import Dialog from "@material-ui/core/Dialog";
import Paper from "@material-ui/core/Paper";
import Input from "@material-ui/core/Input";
import rentalAPI from "./lib/api";
import {deleteCookie, setCookie, getCookie} from "./lib/cookies";

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
function PaperComponent(props) {
  return (
      <Paper {...props} />
  );
}
function App() {
  const classes = useStyles();
  const [loggedIn, setLoggedIn] = useState(!!getCookie("JWT"));
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginModalOpen, setLoginModalOpen] = useState(false);
  function handleLoginClick(){
    if(loggedIn) {
      deleteCookie("JWT");
      setLoggedIn(false);
    }
    else {
      setLoginModalOpen(true)
    }
  }
  function handleModalClose() {
    setLoginModalOpen(false);
  }
  async function loginUser(username, password) {
    const api = new rentalAPI('');
    const response = await api.getToken(username, password);
    if(!!response){
      console.log(response)
      const token = response.data.access;
      setCookie("JWT", token);
      setLoggedIn(true)
      setLoginModalOpen(false)
    }
  }
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
                <Link to="/management">Home</Link>
              </Typography>
              <Button onClick={()=>handleLoginClick()} color="inherit">{loggedIn ? 'Logout' : 'Login'}</Button>
            </Toolbar>
          </AppBar>
          <Dialog
            open={loginModalOpen}
            onClose={handleModalClose}
            PaperComponent={PaperComponent}
            aria-labelledby="draggable-dialog-title"
          >
            <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
              Login
            </DialogTitle>
            <DialogContent>
              <DialogContentText>
                <Input type={"text"} onChange={(e) => setUsername(e.target.value)}/>
                <Input type={"password"} onChange={(e) => setPassword(e.target.value)}/>
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button autoFocus onClick={handleModalClose} color="primary">
                Cancel
              </Button>
              <Button onClick={() => loginUser(username, password)} color="primary">
                Login
              </Button>
            </DialogActions>
          </Dialog>
        </Container>
        {loggedIn && <Container>
            <Switch>
              <Route exact path="/management/" component={Overview}/>
              <Route exact path="/management/products" component={ProductsList}/>
              <Route exact path="/management/products/add" component={ProductAdd}/>
              <Route exact path="/management/products/:id/edit" component={ProductAdd}/>
              <Route exact path="/management/products/:id/detail" component={ProductDetailPage}/>
            </Switch>
        </Container>}
      </Router>
    </ThemeProvider>

    );
}

export default App;
