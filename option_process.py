import pandas as pd
import yfinance as yf
from datetime import datetime

# Load Excel file
file_path = 'Option_Data_Template.xlsx'
df = pd.read_excel(file_path)

print("🔍 Reading option data from Excel...\n")

results = []

for idx, row in df.iterrows():
    try:
        if pd.isna(row['Stock Ticker']) or pd.isna(row['Option Strike Price']) or pd.isna(row['Option Expiration']):
            continue

        # Input values
        ticker = row['Stock Ticker'].upper()
        strike_price = float(row['Option Strike Price'])
        expiration_raw = row['Option Expiration']
        expiration = pd.to_datetime(expiration_raw).strftime('%Y-%m-%d')

        # Fetched data
        stock = yf.Ticker(ticker)
        stock_price = stock.history(period='1d')['Close'].iloc[-1]
        opt_chain = stock.option_chain(expiration)
        puts = opt_chain.puts
        option = puts[puts['strike'] == strike_price]

        if option.empty:
            print(f"⚠️  No option found for {ticker} @ {strike_price} exp {expiration}")
            continue

        premium = option['lastPrice'].values[0]
        delta = option['impliedVolatility'].values[0]  # Approximation

        # Calculated values
        breakeven = strike_price - premium
        downside_pct = ((stock_price - breakeven) / stock_price) * 100
        dte = (pd.to_datetime(expiration_raw) - datetime.today()).days
        annualized_return = (premium / strike_price) * (365 / dte) * 100 if dte > 0 else 0
        collateral = strike_price * 100
        weekly_return_pct = (premium / strike_price) * 100
        weekly_return_dollar = premium * 100
        annual_return_dollar = premium * 52 * 100
        annual_return_pct = weekly_return_pct * 52

        # Console Output
        print(f"\n📌 Row {idx + 2} | {ticker} ${strike_price} exp {expiration}")
        print("\n🔹 Fetched Values:")
        print(f"    💰 Stock Price:         ${stock_price:.2f}")
        print(f"    🧾 Premium:             ${premium:.2f}")
        print(f"    📉 Delta (IV proxy):    {delta:.4f}")

        print("\n🔸 Calculated Metrics:")
        print(f"    🏦 Collateral:          ${collateral:.2f}")
        print(f"    📉 Breakeven:           ${breakeven:.2f}")
        print(f"    ⛔ Downside to B/E:     {downside_pct:.2f}%")
        print(f"    📈 Annualized Return:   {annualized_return:.2f}%")
        print(f"    📆 Weekly Return:       ${weekly_return_dollar:.2f} ({weekly_return_pct:.2f}%)")
        print(f"    📅 Annual Return:       ${annual_return_dollar:.2f} ({annual_return_pct:.2f}%)\n")

        # Save to results
        results.append({
            "Ticker": ticker,
            "Strike Price": strike_price,
            "Expiration": expiration,
            "Stock Price": stock_price,
            "Premium": premium,
            "Delta (IV proxy)": delta,
            "Collateral ($)": collateral,
            "Breakeven ($)": breakeven,
            "Downside to B/E (%)": downside_pct,
            "Annualized Return (%)": annualized_return,
            "Weekly Return ($)": weekly_return_dollar,
            "Weekly Return (%)": weekly_return_pct,
            "Annual Return ($)": annual_return_dollar,
            "Annual Return (%)": annual_return_pct
        })

    except Exception as e:
        print(f"❌ Error in row {idx + 2}: {e}")

# Export
if results:
    result_df = pd.DataFrame(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"Option_Results_{timestamp}.xlsx"
    result_df.to_excel(output_file, index=False)
    print(f"\n✅ Results exported to: {output_file}")
else:
    print("\n⚠️ No valid results to export.")
