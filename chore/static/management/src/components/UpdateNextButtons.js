import React from "react";
import Button from "@material-ui/core/Button";
import myTheme from "../lib/theme";
import makeStyles from "@material-ui/core/styles/makeStyles";

const useStyles = makeStyles(theme => ({
  submitButton: {
    backgroundColor: theme.palette.success.dark,
    width: '50%',
  },
}));
export default function UpdateNextButtons({isEdit, submitStep, currentStep}) {
  const classes = useStyles(myTheme);
  return (
    <>
      <Button
        onClick={() => submitStep(currentStep, false)}
        fullWidth={!isEdit}
        type="submit"
        variant="contained"
        color="primary"
        className={classes.submitButton}>
        Update
      </Button>
      <Button
        onClick={() => submitStep(currentStep + 1, isEdit)}
        fullWidth={!isEdit}
        type="submit"
        variant="contained"
        color="primary"
        className={classes.submitButton}>
          {isEdit ? 'Next' : 'Save'}
      </Button>
    </>
  )
}