import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

try:
    import yfinance as yf
except ImportError:
    yf = None

class OptionAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Call Option Analyzer")

        # Inputs
        ttk.Label(master, text="Ticker:").grid(row=0, column=0, sticky="e")
        self.ticker_entry = ttk.Entry(master, width=10)
        self.ticker_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Expiration (YYYY-MM-DD):").grid(row=1, column=0, sticky="e")
        self.exp_entry = ttk.Entry(master, width=15)
        self.exp_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Strike Price:").grid(row=2, column=0, sticky="e")
        self.strike_entry = ttk.Entry(master, width=10)
        self.strike_entry.grid(row=2, column=1, padx=5, pady=5)

        analyze_btn = ttk.Button(master, text="Analyze", command=self.analyze)
        analyze_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Output area
        self.output = tk.Text(master, height=10, width=60, state="disabled")
        self.output.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Figure placeholder
        self.figure = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

    def analyze(self):
        if yf is None:
            messagebox.showerror("Missing Dependency", "yfinance is not installed.")
            return

        ticker = self.ticker_entry.get().strip().upper()
        exp_date = self.exp_entry.get().strip()
        try:
            strike = float(self.strike_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Strike must be a number")
            return

        try:
            stock = yf.Ticker(ticker)
            stock_price = stock.history(period="1d")['Close'].iloc[-1]
            opt_chain = stock.option_chain(exp_date)
            calls = opt_chain.calls
        except Exception as e:
            messagebox.showerror("Data Error", f"Failed to fetch data: {e}")
            return

        option = calls[calls['strike'] == strike]
        if option.empty:
            messagebox.showinfo("Not Found", "No call option at that strike")
            return

        opt = option.iloc[0]
        premium = (opt['bid'] + opt['ask']) / 2
        breakeven = strike + premium
        delta = opt['impliedVolatility']
        percent_return = (premium / (strike * 100)) * 100
        annual_return = percent_return * 52

        # Display text results
        self.output.configure(state="normal")
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Stock Price: ${stock_price:.2f}\n")
        self.output.insert(tk.END, f"Option Premium: ${premium:.2f}\n")
        self.output.insert(tk.END, f"Breakeven: ${breakeven:.2f}\n")
        self.output.insert(tk.END, f"Delta (IV proxy): {delta:.4f}\n")
        self.output.insert(tk.END, f"% Return: {percent_return:.2f}%\n")
        self.output.insert(tk.END, f"Annualized Return: {annual_return:.2f}%\n")
        self.output.configure(state="disabled")

        # Chart ROI vs Strike
        calls['ROI'] = ((calls['bid'] + calls['ask']) / 2) / (calls['strike'] * 100) * 100
        self.ax.clear()
        self.ax.plot(calls['strike'], calls['ROI'], marker='o')
        self.ax.set_xlabel('Strike Price')
        self.ax.set_ylabel('ROI (%)')
        self.ax.set_title(f'ROI vs Strike for {exp_date}')
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = OptionAnalyzerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
