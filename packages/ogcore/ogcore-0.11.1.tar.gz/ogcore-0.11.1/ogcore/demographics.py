"""
------------------------------------------------------------------------
Functions for generating demographic objects necessary for the OG-USA
model
------------------------------------------------------------------------
"""

# Import packages
import os
import numpy as np
import scipy.optimize as opt
import pandas as pd
import matplotlib.pyplot as plt
from ogcore.utils import get_legacy_session
from ogcore import parameter_plots as pp

START_YEAR = 2023
END_YEAR = 2023
UN_COUNTRY_CODE = "840"  # UN code for USA
# create output director for figures
CUR_PATH = os.path.split(os.path.abspath(__file__))[0]
OUTPUT_DIR = os.path.join(CUR_PATH, "..", "data", "OUTPUT", "Demographics")
if os.access(OUTPUT_DIR, os.F_OK) is False:
    os.makedirs(OUTPUT_DIR)


"""
------------------------------------------------------------------------
Define functions
------------------------------------------------------------------------
"""


def get_un_data(
    variable_code,
    country_id=UN_COUNTRY_CODE,
    start_year=START_YEAR,
    end_year=END_YEAR,
):
    """
    This function retrieves data from the United Nations Data Portal API
    for UN population data (see
    https://population.un.org/dataportal/about/dataapi)

    Args:
        variable_code (str): variable code for UN data
        country_id (str): country id for UN data
        start_year (int): start year for UN data
        end_year (int): end year for UN data

    Returns:
        df (Pandas DataFrame): DataFrame of UN data
    """
    target = (
        "https://population.un.org/dataportalapi/api/v1/data/indicators/"
        + variable_code
        + "/locations/"
        + country_id
        + "/start/"
        + str(start_year)
        + "/end/"
        + str(end_year)
    )

    # get data from url
    response = get_legacy_session().get(target)
    # Check if the request was successful before processing
    if response.status_code == 200:
        # Converts call into JSON
        j = response.json()
        # Convert JSON into a pandas DataFrame.
        # pd.json_normalize flattens the JSON to accommodate nested lists
        # within the JSON structure
        df = pd.json_normalize(j["data"])
        # Loop until there are new pages with data
        while j["nextPage"] is not None:
            # Reset the target to the next page
            target = j["nextPage"]
            # call the API for the next page
            response = get_legacy_session().get(target)
            # Convert response to JSON format
            j = response.json()
            # Store the next page in a data frame
            df_temp = pd.json_normalize(j["data"])
            # Append next page to the data frame
            df = pd.concat([df, df_temp])
        # keep just what is needed from data
        df = df[df.variant == "Median"]
        df = df[df.sex == "Both sexes"][["timeLabel", "ageLabel", "value"]]
        df.rename(
            {"timeLabel": "year", "ageLabel": "age"}, axis=1, inplace=True
        )
        df.loc[df.age == "100+", "age"] = 100
        df.age = df.age.astype(int)
        df.year = df.year.astype(int)
        df = df[df.age < 100]  # need to drop 100+ age category
    else:
        print(
            f"Failed to retrieve population data. HTTP status code: {response.status_code}"
        )
        assert False

    return df


def get_fert(
    totpers=100,
    min_age=0,
    max_age=99,
    country_id=UN_COUNTRY_CODE,
    start_year=START_YEAR,
    end_year=END_YEAR,
    graph=False,
    plot_path=None,
):
    """
    This function generates a vector of fertility rates by model period
    age that corresponds to the fertility rate data by age in years.

    Args:
        totpers (int): total number of agent life periods (E+S), >= 3
        min_age (int): age in years at which agents are born, >= 0
        max_age (int): age in years at which agents die with certainty,
            >= 4, < 100 (max age in UN data is 99, 100+ i same group)
        country_id (str): country id for UN data
        start_year (int): start year for UN data
        end_year (int): end year for UN data
        graph (bool): =True if want graphical output
        plot_path (str): path to save fertility rate plot

    Returns:
        fert_rates (Numpy array): fertility rates for each year of data
            and model age
        fig (Matplotlib Figure): figure object if graph=True and plot_path=None

    """
    # initialize fert rates array
    fert_rates_2D = np.zeros((end_year + 1 - start_year, totpers))
    # Read UN data, 1 year at a time
    for y in range(start_year, end_year + 1):
        df = get_un_data("68", country_id=country_id, start_year=y, end_year=y)
        # put in vector
        fert_rates = df.value.values
        # fill in with zeros for ages  < 15 and > 49
        # NOTE: this assumes min_year < 15 and max_age > 49
        fert_rates = np.append(fert_rates, np.zeros(max_age - 49))
        fert_rates = np.append(np.zeros(15 - min_age), fert_rates)
        # divide by 1000 because fertility rates are number of births per
        # 1000 woman and we want births per person (might update to account
        # from fraction men more correctly - below assumes 50/50 men and women)
        fert_rates = fert_rates / 2000
        # Rebin data in the case that model period not equal to one calendar
        # year
        fert_rates = pop_rebin(fert_rates, totpers)
        fert_rates_2D[y - start_year, :] = fert_rates

    # Create plots if needed
    if graph:
        if plot_path:
            pp.plot_fert_rates(
                fert_rates_2D,
                start_year,
                [start_year, end_year],
                path=plot_path,
            )
            return fert_rates_2D
        else:
            fig = pp.plot_fert_rates(
                fert_rates_2D,
                start_year,
                [start_year, end_year],
            )
            return fert_rates_2D, fig
    else:
        return fert_rates_2D


def get_mort(
    totpers=100,
    min_age=0,
    max_age=99,
    country_id=UN_COUNTRY_CODE,
    start_year=START_YEAR,
    end_year=END_YEAR,
    graph=False,
    plot_path=None,
):
    """
    This function generates a vector of mortality rates by model period
    age.

    Args:
        totpers (int): total number of agent life periods (E+S), >= 3
        min_age (int): age in years at which agents are born, >= 0
        max_age (int): age in years at which agents die with certainty,
            >= 4, < 100 (max age in UN data is 99, 100+ i same group)
        country_id (str): country id for UN data
        start_year (int): start year for UN data
        end_year (int): end year for UN data
        graph (bool): =True if want graphical output
        plot_path (str): path to save mortality rate plot

    Returns:
        mort_rates (Numpy array) mortality rates for each year of data
            and model age
        infmort_rate_vec (Numpy array): infant mortality rates for each
        fig (Matplotlib Figure): figure object if graph=True and plot_path=None

    """
    mort_rates_2D = np.zeros((end_year + 1 - start_year, totpers))
    infmort_rate_vec = np.zeros(end_year + 1 - start_year)
    # Read UN data
    for y in range(start_year, end_year + 1):
        df = get_un_data("80", country_id=country_id, start_year=y, end_year=y)
        # put in vector
        mort_rates_data = df.value.values
        # In UN data, mortality rates for 0 year olds are the infant
        # mortality rates
        infmort_rate = mort_rates_data[0]
        # Rebin data in the case that model period not equal to one calendar
        # year
        # make mort rates those from age 1-100 and set to 1 for age 100
        mort_rates_data = np.append(mort_rates_data[1:], 1.0)
        mort_rates = pop_rebin(mort_rates_data, totpers)
        # put in 2D array
        mort_rates_2D[y - start_year, :] = mort_rates
        infmort_rate_vec[y - start_year] = infmort_rate

    # Create plots if needed
    if graph:
        if plot_path:
            pp.plot_mort_rates_data(
                mort_rates_2D,
                start_year,
                [start_year, end_year],
                path=plot_path,
            )
            return mort_rates_2D, infmort_rate_vec
        else:
            fig = pp.plot_mort_rates_data(
                mort_rates_2D,
                start_year,
                [start_year, end_year],
            )
            return mort_rates_2D, infmort_rate_vec, fig
    else:
        return mort_rates_2D, infmort_rate_vec


def get_pop(
    E=20,
    S=80,
    min_age=0,
    max_age=99,
    country_id=UN_COUNTRY_CODE,
    start_year=START_YEAR,
    end_year=END_YEAR,
):
    """
    Retrives the population distribution data from the UN data API

    Args:
        E (int): number of model periods in which agent is not
            economically active, >= 1
        S (int): number of model periods in which agent is economically
            active, >= 3
        min_age (int): age in years at which agents are born, >= 0
        max_age (int): age in years at which agents die with certainty,
            >= 4, < 100 (max age in UN data is 99, 100+ i same group)
        country_id (str): country id for UN data
        start_year (int): start year data
        end_year (int): end year for data

    Returns:
        pop_2D (Numpy array): population distribution over T0 periods
        pre_pop (Numpy array): population distribution one year before
            initial year for calibration of omega_S_preTP
    """
    # Generate time path of the nonstationary population distribution
    # Get path up to end of data year
    pop_2D = np.zeros((end_year + 1 - start_year + 1, E + S))
    # Read UN data
    for y in range(start_year, end_year + 2):
        pop_data = get_un_data(
            "47",
            country_id=country_id,
            start_year=y,
            end_year=y,
        )
        pop_data_sample = pop_data[
            (pop_data["age"] >= min_age) & (pop_data["age"] <= max_age)
        ]
        pop = pop_data_sample.value.values
        # Generate the current population distribution given that E+S might
        # be less than max_age-min_age+1
        # age_per_EpS = np.arange(1, E + S + 1)
        pop_EpS = pop_rebin(pop, E + S)
        pop_2D[y - start_year, :] = pop_EpS
    # get population distribution one year before initial year for
    # calibration of omega_S_preTP
    pre_pop_data = get_un_data(
        "47",
        country_id=country_id,
        start_year=start_year - 1,
        end_year=start_year - 1,
    )
    pre_pop_sample = pre_pop_data[
        (pre_pop_data["age"] >= min_age) & (pre_pop_data["age"] <= max_age)
    ]
    pre_pop = pre_pop_sample.value.values

    return pop_2D, pre_pop


def pop_rebin(curr_pop_dist, totpers_new):
    """
    For cases in which totpers (E+S) is less than the number of periods
    in the population distribution data, this function calculates a new
    population distribution vector with totpers (E+S) elements.

    Args:
        curr_pop_dist (Numpy array): population distribution over N
            periods
        totpers_new (int): number of periods to which we are
            transforming the population distribution, >= 3

    Returns:
        curr_pop_new (Numpy array): new population distribution over
            totpers (E+S) periods that approximates curr_pop_dist

    """
    # Number of periods in original data
    assert totpers_new >= 3

    # Number of periods in original data
    totpers_orig = len(curr_pop_dist)
    if int(totpers_new) == totpers_orig:
        curr_pop_new = curr_pop_dist
    elif int(totpers_new) < totpers_orig:
        num_sub_bins = float(10000)
        curr_pop_sub = np.repeat(
            np.float64(curr_pop_dist) / num_sub_bins, num_sub_bins
        )
        len_subbins = (np.float64(totpers_orig * num_sub_bins)) / totpers_new
        curr_pop_new = np.zeros(totpers_new, dtype=np.float64)
        end_sub_bin = 0
        for i in range(totpers_new):
            beg_sub_bin = int(end_sub_bin)
            end_sub_bin = int(np.rint((i + 1) * len_subbins))
            curr_pop_new[i] = curr_pop_sub[beg_sub_bin:end_sub_bin].sum()
        # Return curr_pop_new to single precision float (float32)
        # datatype
        curr_pop_new = np.float32(curr_pop_new)

    return curr_pop_new


def get_imm_rates(
    totpers=100,
    min_age=0,
    max_age=99,
    fert_rates=None,
    mort_rates=None,
    infmort_rates=None,
    pop_dist=None,
    country_id=UN_COUNTRY_CODE,
    start_year=START_YEAR,
    end_year=END_YEAR,
    graph=False,
    plot_path=None,
):
    """
    Calculate immigration rates by age as a residual given population
    levels in different periods, then output average calculated
    immigration rate. We have to replace the first mortality rate in
    this function in order to adjust the first implied immigration rate

    Args:
        totpers (int): total number of agent life periods (E+S), >= 3
        min_age (int): age in years at which agents are born, >= 0
        max_age (int): age in years at which agents die with certainty,
            >= 4
        fert_rates (Numpy array): fertility rates for each year of data
            and model age
        mort_rates (Numpy array): mortality rates for each year of data
            and model age
        infmort_rates (Numpy array): infant mortality rates for each year
            of data
        pop_dist (Numpy array): population distribution over T0+1 periods
        country_id (str): country id for UN data
        start_year (int): start year for UN data
        end_year (int): end year for UN data
        graph (bool): =True if want graphical output
        plot_path (str): path to save figure to

    Returns:
        imm_rates_2D (Numpy array):immigration rates that correspond to
            each year of data and period of life, length E+S

    """
    imm_rates_2D = np.zeros((end_year + 1 - start_year, totpers))
    if fert_rates is None:
        # get fert rates from UN data from initial year to data year
        fert_rates = get_fert(
            totpers, min_age, max_age, country_id, start_year, end_year
        )
    else:
        # ensure that user provided fert_rates and mort rates of same size
        assert fert_rates.shape == mort_rates.shape
    if mort_rates is None:
        # get mort rates from UN data from initial year to data year
        mort_rates, infmort_rates = get_mort(
            totpers, min_age, max_age, country_id, start_year, end_year
        )
    else:
        # ensure that user provided fert_rates and mort rates of same size
        assert fert_rates.shape == mort_rates.shape
        assert infmort_rates is not None
        assert infmort_rates.shape[0] == mort_rates.shape[0]
    # Read UN data
    for y in range(start_year, end_year + 1):
        if pop_dist is None:
            # need to read UN population data by age for each year
            df = get_un_data(
                "47", country_id=country_id, start_year=y, end_year=y
            )
            pop_t = df[(df.age < 100) & (df.age >= 0)].value.values
            pop_t = pop_rebin(pop_t, totpers)
            df = get_un_data(
                "47", country_id=country_id, start_year=y + 1, end_year=y + 1
            )
            pop_tp1 = df[(df.age < 100) & (df.age >= 0)].value.values
            pop_tp1 = pop_rebin(pop_tp1, totpers)
        else:
            # Make sure shape conforms
            assert pop_dist.shape[1] == mort_rates.shape[1]
            pop_t = pop_dist[y - start_year, :]
            pop_tp1 = pop_dist[y - start_year + 1, :]
        # initialize imm_rate vector
        imm_rates = np.zeros(totpers)
        # back out imm rates by age for each year
        newborns = np.dot(fert_rates[y - start_year, :], pop_t)
        # new born imm_rate
        imm_rates[0] = (
            pop_tp1[0] - (1 - infmort_rates[y - start_year]) * newborns
        ) / pop_t[0]
        # all other age imm_rates
        imm_rates[1:] = (
            pop_tp1[1:] - (1 - mort_rates[y - start_year, :-1]) * pop_t[:-1]
        ) / pop_t[1:]

        imm_rates_2D[y - start_year, :] = imm_rates

    # Create plots if needed
    if graph:
        if plot_path:
            pp.plot_imm_rates(
                imm_rates_2D,
                start_year,
                [start_year, end_year],
                path=plot_path,
            )
            return imm_rates_2D
        else:
            fig = pp.plot_imm_rates(
                imm_rates_2D,
                start_year,
                [start_year, end_year],
            )
            return imm_rates_2D, fig
    else:
        return imm_rates_2D


def immsolve(imm_rates, *args):
    """
    This function generates a vector of errors representing the
    difference in two consecutive periods stationary population
    distributions. This vector of differences is the zero-function
    objective used to solve for the immigration rates vector, similar to
    the original immigration rates vector from get_imm_rates(), that
    sets the steady-state population distribution by age equal to the
    population distribution in period int(1.5*S)

    Args:
        imm_rates (Numpy array):immigration rates that correspond to
            each period of life, length E+S
        args (tuple): (fert_rates, mort_rates, infmort_rates, omega_cur,
            g_n_SS)

    Returns:
        omega_errs (Numpy array): difference between omega_new and
            omega_cur_pct, length E+S

    """
    fert_rates, mort_rates, infmort_rates, omega_cur_lev, g_n_SS = args
    omega_cur_pct = omega_cur_lev / omega_cur_lev.sum()
    totpers = len(fert_rates)
    OMEGA = np.zeros((totpers, totpers))
    OMEGA[0, :] = (1 - infmort_rates) * fert_rates + np.hstack(
        (imm_rates[0], np.zeros(totpers - 1))
    )
    OMEGA[1:, :-1] += np.diag(1 - mort_rates[:-1])
    OMEGA[1:, 1:] += np.diag(imm_rates[1:])
    omega_new = np.dot(OMEGA, omega_cur_pct) / (1 + g_n_SS)
    omega_errs = omega_new - omega_cur_pct

    return omega_errs


def get_pop_objs(
    E=20,
    S=80,
    T=320,
    min_age=0,
    max_age=99,
    fert_rates=None,
    mort_rates=None,
    infmort_rates=None,
    imm_rates=None,
    pop_dist=None,
    pre_pop_dist=None,
    country_id=UN_COUNTRY_CODE,
    initial_data_year=START_YEAR - 1,
    final_data_year=START_YEAR + 2,  # as default data year goes until T1
    GraphDiag=True,
):
    """
    This function produces the demographics objects to be used in the
    OG-USA model package.

    Args:
        E (int): number of model periods in which agent is not
            economically active, >= 1
        S (int): number of model periods in which agent is economically
            active, >= 3
        T (int): number of periods to be simulated in TPI, > 2*S
        min_age (int): age in years at which agents are born, >= 0
        max_age (int): age in years at which agents die with certainty,
            >= 4, < 100 (max age in UN data is 99, 100+ i same group)
        fert_rates (array_like): user provided fertility rates, dimensions
            are T0 x E+S
        mort_rates (array_like): user provided mortality rates, dimensions
            are T0 x E+S
        infmort_rates (array_like): user provided infant mortality rates,
            length T0
        imm_rates (array_like): user provided immigration rates, dimensions
            are T0 x E+S
        pop_dist (array_like): user provided population distribution,
            dimensions are T0+1 x E+S
        pre_pop_dist (array_like): user provided population distribution
            for the year before the initial year for calibration,
            length E+S
        country_id (str): country id for UN data
        initial_data_year (int): initial year of data to use
            (not relevant if have user provided data)
        final_data_year (int): final year of data to use,
            T0=intial_year-final_year + 1
        pop_dist (array_like): user provided population distribution, last
            dimension is of length E+S
        GraphDiag (bool): =True if want graphical output and printed
                diagnostics

    Returns:
        pop_dict (dict): includes:
            omega_path_S (Numpy array), time path of the population
                distribution from the current state to the steady-state,
                size T+S x S
            g_n_SS (scalar): steady-state population growth rate
            omega_SS (Numpy array): normalized steady-state population
                distribution, length S
            surv_rates (Numpy array): survival rates that correspond to
                each model period of life, length S
            mort_rates (Numpy array): mortality rates that correspond to
                each model period of life, length S
            g_n_path (Numpy array): population growth rates over the time
                path, length T + S

    """
    # TODO: this function does not generalize with T.
    # It assumes one model period is equal to one calendar year in the
    # time dimesion (it does adjust for S, however)
    T0 = (
        final_data_year - initial_data_year + 1
    )  # number of periods until constant fertility and mortality rates
    print(
        "Demographics data: Initial Data year = ",
        initial_data_year,
        ", Final Data year = ",
        final_data_year,
    )
    assert E + S <= max_age - min_age + 1
    assert initial_data_year >= 2011 and initial_data_year <= 2100
    assert final_data_year >= 2011 and final_data_year <= 2100
    # Ensure that the last year of data used is before SS transition assumed
    # Really, it will need to be well before this
    assert final_data_year > initial_data_year
    assert final_data_year < initial_data_year + T
    assert (
        T > 2 * T0
    )  # ensure time path 2x as long as allows rates to fluctuate

    # Get fertility rates if not provided
    if fert_rates is None:
        # get fert rates from UN data from initial year to data year
        fert_rates = get_fert(
            E + S,
            min_age,
            max_age,
            country_id,
            initial_data_year,
            final_data_year,
        )
    else:
        # ensure that user provided fert_rates are of the correct shape
        assert fert_rates.shape[0] == T0
        assert fert_rates.shape[-1] == E + S
    # Extrapolate fertility rates for the rest of the transition path
    # the implicit assumption is that they are constant after the
    # last year of UN or user provided data
    fert_rates = np.concatenate(
        (
            fert_rates,
            np.tile(
                fert_rates[-1, :].reshape(1, E + S),
                (T - fert_rates.shape[0], 1),
            ),
        ),
        axis=0,
    )
    # Get mortality rates if not provided
    if mort_rates is None:
        # get mort rates from UN data from initial year to data year
        mort_rates, infmort_rates = get_mort(
            E + S,
            min_age,
            max_age,
            country_id,
            initial_data_year,
            final_data_year,
        )
    else:
        # ensure that user provided mort_rates are of the correct shape
        assert mort_rates.shape[0] == T0
        assert mort_rates.shape[-1] == E + S
        assert infmort_rates is not None
        assert infmort_rates.shape[0] == mort_rates.shape[0]
    # Extrapolate mortality rates for the rest of the transition path
    # the implicit assumption is that they are constant after the
    # last year of UN or user provided data
    mort_rates = np.concatenate(
        (
            mort_rates,
            np.tile(
                mort_rates[-1, :].reshape(1, E + S),
                (T - mort_rates.shape[0], 1),
            ),
        ),
        axis=0,
    )
    infmort_rates = np.concatenate(
        (
            infmort_rates,
            np.tile(infmort_rates[-1], (T - infmort_rates.shape[0])),
        )
    )
    mort_rates_S = mort_rates[:, E:]
    # Get population distribution if not provided
    if pop_dist is None:
        pop_2D, pre_pop = get_pop(
            E,
            S,
            min_age,
            max_age,
            country_id,
            initial_data_year,
            final_data_year,
        )
    else:
        # Check first dims of pop_dist as input by user
        assert pop_dist.shape[0] == T0 + 1  # population needs to be
        # one year longer in order to find immigration rates
        assert pop_dist.shape[-1] == E + S
        # Check that pre_pop specified
        assert pre_pop_dist is not None
        assert pre_pop_dist.shape[0] == pop_dist.shape[1]
        pre_pop = pre_pop_dist
        # Create 2D array of population distribution
        pop_2D = np.zeros((T0 + 1, E + S))
        for t in range(T0 + 1):
            pop_EpS = pop_rebin(pop_dist[t, :], E + S)
            pop_2D[t, :] = pop_EpS
    # Get percentage distribution for S periods for pre-TP period
    pre_pop_EpS = pop_rebin(pre_pop, E + S)
    # Get immigration rates if not provided
    if imm_rates is None:
        imm_rates_orig = get_imm_rates(
            E + S,
            min_age,
            max_age,
            fert_rates,
            mort_rates,
            infmort_rates,
            pop_2D,
            country_id,
            initial_data_year,
            final_data_year,
        )
    else:
        # ensure that user provided imm_rates are of the correct shape
        assert imm_rates.shape[0] == T0
        assert imm_rates.shape[-1] == E + S
        imm_rates_orig = imm_rates
    # Extrapolate immigration rates for the rest of the transition path
    # the implicit assumption is that they are constant after the
    # last year of UN or user provided data
    imm_rates_orig = np.concatenate(
        (
            imm_rates_orig,
            np.tile(
                imm_rates_orig[-1, :].reshape(1, E + S),
                (T - imm_rates_orig.shape[0], 1),
            ),
        ),
        axis=0,
    )
    # If the population distribution was given, check it for consistency
    # with the fertility, mortality, and immigration rates
    if pop_dist is not None:
        len_pop_dist = pop_dist.shape[0]
        pop_counter_2D = np.zeros((len_pop_dist, E + S))
        # set initial population distribution in the counterfactual to
        # the first year of the user provided distribution
        pop_counter_2D[0, :] = pop_dist[0, :]
        for t in range(1, len_pop_dist):
            # find newborns next period
            newborns = np.dot(fert_rates[t - 1, :], pop_counter_2D[t - 1, :])

            pop_counter_2D[t, 0] = (
                1 - infmort_rates[t - 1]
            ) * newborns + imm_rates[t - 1, 0] * pop_counter_2D[t - 1, 0]
            pop_counter_2D[t, 1:] = (
                pop_counter_2D[t - 1, :-1] * (1 - mort_rates[t - 1, :-1])
                + pop_counter_2D[t - 1, 1:] * imm_rates_orig[t - 1, 1:]
            )
        # Check that counterfactual pop dist is close to pop dist given
        assert np.allclose(pop_counter_2D, pop_dist)
    # Create the transition matrix for the population distribution
    # from T0 going forward (i.e., past when we have data on forecasts)
    OMEGA_orig = np.zeros((E + S, E + S))
    OMEGA_orig[0, :] = (1 - infmort_rates[-1]) * fert_rates[-1, :] + np.hstack(
        (imm_rates_orig[-1, 0], np.zeros(E + S - 1))
    )
    OMEGA_orig[1:, :-1] += np.diag(1 - mort_rates[-1, :-1])
    OMEGA_orig[1:, 1:] += np.diag(imm_rates_orig[-1, 1:])

    # Solve for steady-state population growth rate and steady-state
    # population distribution by age using eigenvalue and eigenvector
    # decomposition
    eigvalues, eigvectors = np.linalg.eig(OMEGA_orig)
    g_n_SS = (eigvalues[np.isreal(eigvalues)].real).max() - 1
    eigvec_raw = eigvectors[
        :, (eigvalues[np.isreal(eigvalues)].real).argmax()
    ].real
    omega_SS_orig = eigvec_raw / eigvec_raw.sum()

    # Generate time path of the population distribution after final
    # year of data
    omega_path_lev = np.zeros((T + S, E + S))
    pop_curr = pop_2D[T0 - 1, :]
    omega_path_lev[:T0, :] = pop_2D[:T0, :]
    for per in range(T0, T + S):
        pop_next = np.dot(OMEGA_orig, pop_curr)
        omega_path_lev[per, :] = pop_next.copy()
        pop_curr = pop_next.copy()

    # Force the population distribution after 1.5*S periods to be the
    # steady-state distribution by adjusting immigration rates, holding
    # constant mortality, fertility, and SS growth rates
    imm_tol = 1e-14
    fixper = int(1.5 * S + T0)
    omega_SSfx = omega_path_lev[fixper, :] / omega_path_lev[fixper, :].sum()
    imm_objs = (
        fert_rates[fixper, :],
        mort_rates[fixper, :],
        infmort_rates[fixper],
        omega_path_lev[fixper, :],
        g_n_SS,
    )
    imm_fulloutput = opt.fsolve(
        immsolve,
        imm_rates_orig[fixper, :],
        args=(imm_objs),
        full_output=True,
        xtol=imm_tol,
    )
    imm_rates_adj = imm_fulloutput[0]
    imm_diagdict = imm_fulloutput[1]
    omega_path_S = omega_path_lev[:, -S:] / (
        omega_path_lev[:, -S:].sum(axis=1).reshape((T + S, 1))
    )
    omega_path_S[fixper:, :] = np.tile(
        omega_path_S[fixper, :].reshape((1, S)), (T + S - fixper, 1)
    )
    g_n_path = np.zeros(T + S)
    g_n_path[1:] = (
        omega_path_lev[1:, -S:].sum(axis=1)
        - omega_path_lev[:-1, -S:].sum(axis=1)
    ) / omega_path_lev[:-1, -S:].sum(axis=1)
    g_n_path[0] = (
        omega_path_lev[0, -S:].sum() - pre_pop_EpS[-S:].sum()
    ) / pre_pop_EpS[-S:].sum()
    g_n_path[fixper + 1 :] = g_n_SS
    omega_S_preTP = pre_pop_EpS[-S:] / pre_pop_EpS[-S:].sum()
    imm_rates_mat = np.concatenate(
        (
            imm_rates_orig[:fixper, E:],
            np.tile(
                imm_rates_adj[E:].reshape(1, S),
                (T - fixper, 1),
            ),
        ),
        axis=0,
    )

    if GraphDiag:
        # Check whether original SS population distribution is close to
        # the period-T population distribution
        omegaSSmaxdif = np.absolute(
            omega_SS_orig - (omega_path_lev[T, :] / omega_path_lev[T, :].sum())
        ).max()
        if omegaSSmaxdif > 0.0003:
            print(
                "POP. WARNING: Max. abs. dist. between original SS "
                + "pop. dist'n and period-T pop. dist'n is greater than"
                + " 0.0003. It is "
                + str(omegaSSmaxdif)
                + "."
            )
        else:
            print(
                "POP. SUCCESS: orig. SS pop. dist is very close to "
                + "period-T pop. dist'n. The maximum absolute "
                + "difference is "
                + str(omegaSSmaxdif)
                + "."
            )

        # Plot the adjusted steady-state population distribution versus
        # the original population distribution. The difference should be
        # small
        omegaSSvTmaxdiff = np.absolute(omega_SS_orig - omega_SSfx).max()
        if omegaSSvTmaxdiff > 0.0003:
            print(
                "POP. WARNING: The maximum absolute difference "
                + "between any two corresponding points in the original"
                + " and adjusted steady-state population "
                + "distributions is"
                + str(omegaSSvTmaxdiff)
                + ", "
                + "which is greater than 0.0003."
            )
        else:
            print(
                "POP. SUCCESS: The maximum absolute difference "
                + "between any two corresponding points in the original"
                + " and adjusted steady-state population "
                + "distributions is "
                + str(omegaSSvTmaxdiff)
            )

        # Print whether or not the adjusted immigration rates solved the
        # zero condition
        immtol_solved = np.absolute(imm_diagdict["fvec"].max()) < imm_tol
        if immtol_solved:
            print(
                "POP. SUCCESS: Adjusted immigration rates solved "
                + "with maximum absolute error of "
                + str(np.absolute(imm_diagdict["fvec"].max()))
                + ", which is less than the tolerance of "
                + str(imm_tol)
            )
        else:
            print(
                "POP. WARNING: Adjusted immigration rates did not "
                + "solve. Maximum absolute error of "
                + str(np.absolute(imm_diagdict["fvec"].max()))
                + " is greater than the tolerance of "
                + str(imm_tol)
            )

        # Test whether the steady-state growth rates implied by the
        # adjusted OMEGA matrix equals the steady-state growth rate of
        # the original OMEGA matrix
        OMEGA2 = np.zeros((E + S, E + S))
        OMEGA2[0, :] = (1 - infmort_rates[-1]) * fert_rates[-1, :] + np.hstack(
            (imm_rates_adj[0], np.zeros(E + S - 1))
        )
        OMEGA2[1:, :-1] += np.diag(1 - mort_rates[-1, :-1])
        OMEGA2[1:, 1:] += np.diag(imm_rates_adj[1:])
        eigvalues2, eigvectors2 = np.linalg.eig(OMEGA2)
        g_n_SS_adj = (eigvalues[np.isreal(eigvalues2)].real).max() - 1
        if np.max(np.absolute(g_n_SS_adj - g_n_SS)) > 10 ** (-8):
            print(
                "FAILURE: The steady-state population growth rate"
                + " from adjusted OMEGA is different (diff is "
                + str(g_n_SS_adj - g_n_SS)
                + ") than the steady-"
                + "state population growth rate from the original"
                + " OMEGA."
            )
        elif np.max(np.absolute(g_n_SS_adj - g_n_SS)) <= 10 ** (-8):
            print(
                "SUCCESS: The steady-state population growth rate"
                + " from adjusted OMEGA is close to (diff is "
                + str(g_n_SS_adj - g_n_SS)
                + ") the steady-"
                + "state population growth rate from the original"
                + " OMEGA."
            )

        # Do another test of the adjusted immigration rates. Create the
        # new OMEGA matrix implied by the new immigration rates. Plug in
        # the adjusted steady-state population distribution. Hit is with
        # the new OMEGA transition matrix and it should return the new
        # steady-state population distribution
        omega_new = np.dot(OMEGA2, omega_SSfx)
        omega_errs = np.absolute(omega_new - omega_SSfx)
        print(
            "The maximum absolute difference between the adjusted "
            + "steady-state population distribution and the "
            + "distribution generated by hitting the adjusted OMEGA "
            + "transition matrix is "
            + str(omega_errs.max())
        )

        # Plot the original immigration rates versus the adjusted
        # immigration rates
        immratesmaxdiff = np.absolute(imm_rates_orig - imm_rates_adj).max()
        print(
            "The maximum absolute distance between any two points "
            + "of the original immigration rates and adjusted "
            + "immigration rates is "
            + str(immratesmaxdiff)
        )

        # plots
        age_per_EpS = np.arange(1, E + S + 1)
        pp.plot_omega_fixed(
            age_per_EpS, omega_SS_orig, omega_SSfx, E, S, path=OUTPUT_DIR
        )
        pp.plot_imm_fixed(
            age_per_EpS,
            imm_rates_orig[fixper - 1, :],
            imm_rates_adj,
            E,
            S,
            path=OUTPUT_DIR,
        )
        pp.plot_population_path(
            age_per_EpS,
            omega_path_lev,
            omega_SSfx,
            initial_data_year,
            initial_data_year,
            initial_data_year,
            S,
            path=OUTPUT_DIR,
        )

    # return omega_path_S, g_n_SS, omega_SSfx, survival rates,
    # mort_rates_S, and g_n_path
    pop_dict = {
        "omega": omega_path_S,
        "g_n_ss": g_n_SS,
        "omega_SS": omega_SSfx[-S:] / omega_SSfx[-S:].sum(),
        "rho": [mort_rates_S],
        "g_n": g_n_path,
        "imm_rates": imm_rates_mat,
        "omega_S_preTP": omega_S_preTP,
    }

    return pop_dict
