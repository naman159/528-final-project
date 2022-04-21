import React from 'react';
import { useState } from 'react';
import Select from 'react-select';

// material-ui
import { Grid, Typography } from '@material-ui/core';

// project imports
import MainCard from '../../ui-component/cards/MainCard';

const sensorPositions = [
  { label: "Left", value: 1 },
  { label: "Right", value: 2 }
];

//==============================|| SAMPLE PAGE ||==============================//

const SamplePage = () => {
    const handleSubmit = event => {
        event.preventDefault();
        console.log(leftFile);
        console.log(rightFile)

        alert('You have submitted the form.')
    };
    const [leftFile, setLeftFile] = useState(null);
    const handleLeftFileChange = e => {
        var read = new FileReader();
        read.readAsBinaryString(e.target.files[0]);
        read.onloadend = function(){
            setLeftFile(read.result);
        }
    }
    const [rightFile, setRightFile] = useState(null);
    const handleRightFileChange = e => {
        var read = new FileReader();
        read.readAsBinaryString(e.target.files[0]);
        read.onloadend = function(){
            setRightFile(read.result);
        }
    }
    return (
        <MainCard title="Upload Calibrex BLE Log">
            <form onSubmit={handleSubmit}>
                <Grid item xs={12}>
                    <Grid container alignItems="center" justifyContent="space-between">
                        <Grid item>
                            <Grid container direction="column" spacing={2}>
                                <Grid item>
                                    <Typography variant="h8">Left sensor log:</Typography>
                                </Grid>
                                <Grid item>
                                    <input type="file" onChange={handleLeftFileChange}/>
                                </Grid>
                                <Grid item>
                                    <Typography variant="h8">Right sensor log:</Typography>
                                </Grid>
                                <Grid item>
                                    <input type="file" onChange={handleRightFileChange}/>
                                </Grid>
                                <Grid item>
                                    <button type="submit">Submit</button>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </form>
        </MainCard>
    );
};

export default SamplePage;
