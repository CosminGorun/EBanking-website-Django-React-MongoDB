import React, { useState, useEffect } from 'react';
import axios from 'axios';
import axiosInstance from '../axiosInstance';
import { useNavigate } from "react-router-dom";
import './mainPage.css'

function EBanking() {
  const [tranzactiiUserOUT, setTranzactiiUserOUT] = useState([]);
  const [tranzactiiUserIN, setTranzactiiUserIN] = useState([]);
  const [transferuriAcceptate, settransferuriAcceptate] = useState([]);
  const [transferuriRejectate, settransferuriRejectate] = useState([]);
  const [conturiIBAN, setConturiIBAN] = useState([]);
  const [contIBAN, setContIBAN] = useState('');
  const [userID, setUserID] = useState('');
  const [userName, setUserName] = useState([]);
  const [cont, setCont] = useState({});
  const [sold, setSold] = useState('')
  const [moneda, setMoneda] = useState('')
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [ibanSursa, setIbanSursa] = useState('');
  const [ibanDestinatie, setIbanDestinatie] = useState('');
  const [suma, setSuma] = useState('');
  const [IDTransfer, setIDTransfer] = useState('');
  const [action, setAction] = useState('');
 const navigate = useNavigate();
  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    axiosInstance.get('/mainPage')
      .then(response => {
        setTranzactiiUserOUT(response.data.tranzactiiUserOUT);
        setTranzactiiUserIN(response.data.tranzactiiUserIN);
        setConturiIBAN(response.data.conturiIBAN)
        setUserID(response.data.USERID);
        setUserName(response.data.NAME);
        setMoneda(response.data.MONEDA);
        setCont(response.data.CONT);
        setSold(cont.sold)
        setIbanSursa(response.data.CONT.iban);
        settransferuriAcceptate(response.data.transferuriAcceptate)
        settransferuriRejectate(response.data.transferuriRejectate)
        if (response.data.conturiIBAN && response.data.conturiIBAN.length > 0) {
        // setContIBAN(response.data.conturiIBAN[0]);
        }
      })
      .catch(err => {
        setError('Error fetching transaction data');
        console.error(err);
      });
  };


  const handleTransfer = async (e) => {
    e.preventDefault();
    try {
      console.log("ibanSursa:", ibanSursa);
      console.log("UserID", userID);
      const response = await axiosInstance.post('/transferConturi', {ibanDestinatie, suma: parseFloat(suma), ibanSursa, userID: parseInt(userID,10) });
      await fetchTransactions();
      setSold(cont.sold)
      console.log("soldul este", cont.sold);
      //await fetchAccountData();
      setSuccessMessage(response.data.message);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error during transfer');
      setSuccessMessage(null);
    }
  };


  const formatMoneda = (monedaValue) => {
    return (Math.round(monedaValue * 100) / 100).toFixed(2);
  };

  const handleTransferAction = async (e, IDTransfer, action) => {
    e.preventDefault();
    try{
    axiosInstance.post('/finalizareTransfer', {
      IDTransfer,
      action
    })
      .then(response => {
        setSuccessMessage(response.data.message);
        setError(null);
        fetchTransactions();
        setSold(cont.sold)
        //console.log("soldul este", cont.sold);
        //fetchAccountData();
      })
    } catch(err) {
        setError(err.response?.data?.error || 'Error processing transfer action');
        setSuccessMessage(null);
      };
  };

  const handlegetTransfer = async (e) => {
    e.preventDefault();
    try{
    axiosInstance.post('/getTransferuri', {
      contIBAN
    })
      .then(response => {
        setSuccessMessage(response.data.message);
        setError(null);
        settransferuriAcceptate(response.data.transferuriAcceptate)
        settransferuriRejectate(response.data.transferuriRejectate)
        //console.log("soldul este", cont.sold);
        //fetchAccountData();
      })
    } catch(err) {
        setError(err.response?.data?.error || 'Error processing transfer action');
        setSuccessMessage(null);
      };
  };

  const handleCancelTransfer = async (e, IDTransfer) => {
    e.preventDefault();
    try{
      axiosInstance.post('/cancelTransfer', { IDTransfer })
      .then(response => {
        setSuccessMessage(response.data.message);
        setError(null);
        fetchTransactions();
        setSold(cont.sold)
        //console.log("soldul este", cont.sold);
        //fetchAccountData();
      })
    } catch(err ) {
        setError(err.response?.data?.error || 'Error canceling transfer');
        setSuccessMessage(null);
      };
  };
  const handleCreateAcc = async (e) => {
  e.preventDefault(); // Prevent default link behavior
  try {
    navigate('/viewMultipleAccounts', { state: { userID } });
  } catch (err) {
    setError(err.response?.data?.error || 'Error initiating account creation');
    setSuccessMessage(null);
  }
};
  const fetchAccountData = async (e) => {
                      setContIBAN(e.target.value);
                      setIbanSursa(e.target.value);
                      // Make API call to change the account based on selected IBAN
                      try {
                          const response = await axiosInstance.get('/gaseste_cont', {
  params: { contIBAN: e.target.value }, // Send contIBAN as query parameters
}).then(response => {
        setTranzactiiUserOUT(response.data.tranzactiiUserOUT);
        setTranzactiiUserIN(response.data.tranzactiiUserIN);
        // setConturiIBAN(response.data.conturiIBAN)
        setUserID(response.data.USERID);
        setUserName(response.data.NAME);
        setCont(response.data.CONT);
        setSold(cont.sold)
        settransferuriAcceptate(response.data.transferuriAcceptate)
        settransferuriRejectate(response.data.transferuriRejectate)
        setMoneda(response.data.MONEDA);
        //console.log("soldul este", cont.sold);
        //fetchAccountData();
      })
                           // Update the `cont` state
                          // setSold(updatedCont.sold);

                      } catch (error) {
                          console.error('Error switching account:', error);
                          setError('Error switching to the selected account');
                      }
  }
  return (
      <div className="container">
          {/* User Info Section */}
          <div className="user-info">
              <h2>Hello {userName} cu id {userID}</h2>
              <p>Soldul contului este {formatMoneda(cont.sold)} {moneda}</p>
              <p>Ibanul contului este {cont.iban}</p>
          </div>
          <div className="iban-dropdown">
              <h3>Select IBAN:</h3>
              <select
                  value={contIBAN}
                  onChange={fetchAccountData}
              >
                  <option value="">Select an IBAN</option>
                  {conturiIBAN && conturiIBAN.length > 0 ? (
                      conturiIBAN.map((iban, index) => (
                          <option key={index} value={iban}>
                              {iban}
                          </option>
                      ))
                  ) : (
                      <option value="">No IBANs available</option>
                  )}
              </select>
          </div>

          <form action="transferConturi" method="post">
              <input type="text" name="ibanDestinatie" placeholder="Iban Destinatie" value={ibanDestinatie}
                     onChange={(e) => setIbanDestinatie(e.target.value)}/>
              <input type="text" name="suma" placeholder="Suma" value={suma} onChange={(e) => setSuma(e.target.value)}/>
              <input type="hidden" name="ibanSursa"/>
              <input type="hidden" name="userID"/>
              <button onClick={handleTransfer} type="submit" value="Transfer"> Transfer</button>
          </form>
          {error && <div className="error-message">{error}</div>}

          <div className="transactions">
              <h2>Tranzactii primite</h2>
              {tranzactiiUserOUT.length > 0 ? (
                  tranzactiiUserOUT.map((transaction, index) => (
                      <form key={index} action="finalizareTransfer" method="post">
                          <div>
                              <p>IBAN primire: {transaction.IBANtrimite}</p>
                              <p>Suma: {transaction.sumaTransfer} {transaction.moneda}</p>
                              <p>Data: {transaction.dataTranzactiei}</p>
                              <input type="hidden" name="IDTransfer" value={transaction.IDTransfer}/>
                              <button onClick={(e) => handleTransferAction(e, transaction.IDTransfer, 'accept')}
                                      type="submit" name="action" value="accept">Accepta bani
                              </button>
                              <button onClick={(e) => handleTransferAction(e, transaction.IDTransfer, 'reject')}
                                      type="submit" name="action" value="reject">Respinge transferul
                              </button>
                          </div>
                      </form>
                  ))
              ) : (
                  <p>No incoming transactions.</p>
              )}
          </div>
          <div className="transactions">
              <h2>Tranzactii trimise</h2>
              {tranzactiiUserIN.length > 0 ? (
                  tranzactiiUserIN.map((transaction, index) => (
                      <form key={index} action="cancelTransfer" method="post">
                          <div>
                              <p>IBAN trimitere: {transaction.IBANprimeste}</p>
                              <p>Suma: {transaction.sumaTransfer} {transaction.moneda}</p>
                              <p>Data: {transaction.dataTranzactiei}</p>
                              <input type="hidden" name="IDTransfer" value={transaction.IDTransfer}/>
                              <button onClick={(e) => handleCancelTransfer(e, transaction.IDTransfer)}
                                      type="submit">Cancel
                              </button>
                          </div>
                      </form>
                  ))
              ) : (
                  <p>No outgoing transactions.</p>
              )}
          </div>
          <div>
              <h2>Received Transfers</h2>
              <table className="styled-table">
                  <thead>
                  <tr>
                      <th>ID Transfer</th>
                      <th>Source IBAN</th>
                      <th>Destination IBAN</th>
                      <th>Amount</th>
                      <th>Currency</th>
                      <th>Transaction Date</th>
                      <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  {transferuriAcceptate.map((transfer, index) => (
                      <tr key={index}>
                          <td>{transfer.IDTransfer}</td>
                          <td>{transfer.IBANtrimite}</td>
                          <td>{transfer.IBANprimeste}</td>
                          <td>{formatMoneda(transfer.sumaTransfer)}</td>
                          <td>{transfer.moneda}</td>
                          <td>{transfer.dataTranzactiei}</td>
                          <td>{transfer.finalizat==1 ? "Finalised" : "Canceled"}</td>
                      </tr>
                  ))}
                  </tbody>
              </table>

              <h2>Sent Transfers</h2>
              <table className="styled-table">
                  <thead>
                  <tr>
                      <th>ID Transfer</th>
                      <th>Source IBAN</th>
                      <th>Destination IBAN</th>
                      <th>Amount</th>
                      <th>Currency</th>
                      <th>Transaction Date</th>
                      <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  {transferuriRejectate.map((transfer, index) => (
                      <tr key={index}>
                          <td>{transfer.IDTransfer}</td>
                          <td>{transfer.IBANtrimite}</td>
                          <td>{transfer.IBANprimeste}</td>
                          <td>{formatMoneda(transfer.sumaTransfer)}</td>
                          <td>{transfer.moneda}</td>
                          <td>{transfer.dataTranzactiei}</td>
                          <td>{transfer.finalizat == 1 ? "Finalised" : "Canceled"}</td>
                      </tr>
                  ))}
                  </tbody>
              </table>
          </div>
          <p className="mltipleacc-bottom-p">
              Vrei inca un cont? <a href="#" onClick={handleCreateAcc}>Creeaza</a>
          </p>
      </div>
  );
}

export default EBanking;
