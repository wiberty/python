import pytest
import pandas as pd
from pma import PMA


@pytest.fixture
def pma_instance():
    return PMA('ticker_list.csv', 'ticker_prices.csv')


def test_analyze_with_incorrect_file_names():
    with pytest.raises(Exception):
        PMA.analyze('ticker_listWRONG.csv', 'ticker_pricesWRONG.csv')
        PMA.analyze('', '')


def test_read_watchlist(pma_instance):
    pma_instance.read_watchlist()
    assert isinstance(pma_instance.watchlist_tickers, list)
    assert len(pma_instance.watchlist_tickers) > 0


def test_read_ticker_prices(pma_instance):
    pma_instance.read_ticker_prices()
    assert isinstance(pma_instance.ticker_prices, pd.DataFrame)
    assert not pma_instance.ticker_prices.empty


def test_filter_data(pma_instance):
    pma_instance.read_watchlist()
    pma_instance.read_ticker_prices()
    pma_instance.filter_data()
    assert isinstance(pma_instance.ticker_prices_f, pd.DataFrame)
    assert not pma_instance.ticker_prices_f.empty
    assert all(ticker in pma_instance.watchlist_tickers for ticker in pma_instance.ticker_prices_f['Ticker'])


def test_calculate_percentage_movements(pma_instance):
    pma_instance.read_watchlist()
    pma_instance.read_ticker_prices()
    pma_instance.filter_data()
    pma_instance.calculate_percentage_movements()
    assert '1 Day %' in pma_instance.ticker_prices_f.columns
    assert '1 Month %' in pma_instance.ticker_prices_f.columns
    assert '1 Year %' in pma_instance.ticker_prices_f.columns


def test_sort_filtered_data(pma_instance):
    pma_instance.read_watchlist()
    pma_instance.read_ticker_prices()
    pma_instance.filter_data()
    pma_instance.calculate_percentage_movements()
    pma_instance.sort_filtered_data()
    assert isinstance(pma_instance.ticker_prices_f_s, pd.DataFrame)
    assert not pma_instance.ticker_prices_f_s.empty
    assert all(rank == index + 1 for index, rank in enumerate(pma_instance.ticker_prices_f_s['Ranking']))


def test_find_negative_tickers(pma_instance):
    pma_instance.read_watchlist()
    pma_instance.read_ticker_prices()
    pma_instance.filter_data()
    pma_instance.calculate_percentage_movements()
    pma_instance.sort_filtered_data()
    pma_instance.find_negative_tickers()
    assert isinstance(pma_instance.negative_tickers, pd.DataFrame)
    assert not pma_instance.negative_tickers.empty
    assert pma_instance.negative_tickers['1 Day %'].lt(0).all()
    assert pma_instance.negative_tickers['1 Month %'].lt(0).all()
    assert pma_instance.negative_tickers['1 Year %'].lt(0).all()


def test_process_unfiltered_data(pma_instance):
    pma_instance.read_ticker_prices()
    pma_instance.process_unfiltered_data()
    assert isinstance(pma_instance.ticker_prices_uf_s, pd.DataFrame)
    assert not pma_instance.ticker_prices_uf_s.empty
    assert len(pma_instance.top_tickers) == pma_instance.nprices # n number of prices returned
    assert all(rank == index + 1 for index, rank in enumerate(pma_instance.top_tickers['Ranking']))


def test_analysis(pma_instance, capsys):
    pma_instance.analysis()
    captured = capsys.readouterr()
    assert "Portfolio Performance:" in captured.out
    assert "Tickers with All Negative % Movements:" in captured.out
    assert f"Top {pma_instance.nprices} Tickers Available:" in captured.out