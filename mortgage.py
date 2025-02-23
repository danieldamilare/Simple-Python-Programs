import numpy as np
import matplotlib.pyplot as plt
class Mortgage:
    """Abstract class for building different kinds of mortgase"""
    def __init__(self, loan, annRate, months):
        self.loan = loan
        self._rate = annRate/12.0
        self._months = months
        self._paid = [0.0]
        self._outstanding = [loan]
        self._payment = find_payment(loan, self._rate, months)
        self.legend = None

    def make_payment(self):
        self._paid.append(self._payment)
        reduction = self._payment - self._outstanding[-1] * self._rate
        self._outstanding.append(self._outstanding[-1] - reduction)

    def get_total_paid(self):
        return sum(self._paid)

    def __str__(self):
        return self.legend

    def plot_payments(self, style):
        plt.plot(self._paid[1:], style, label = self.legend)

    def plot_balance(self, style):
        plt.plot(self._outstanding, style, label = self.legend)

    def plot_tot_pd(self, style):
        tot_pd = [self._paid[0]] + [sum(self._paid[:i+1]) for i in range(1, len(self._paid))]
        plt.plot(tot_pd, style, label = self.legend)

    def plot_net(self, style):
        tot_pd = [self._paid[0]] + [sum(self._paid[:i+1]) for i in range(1, len(self._paid))]
        entity_acquired = np.array([self.loan] * len(self._outstanding))
        entity_acquired = entity_acquired-np.array(self._outstanding)
        net = np.array(tot_pd) - entity_acquired
        plt.plot(net, style, label = self.legend)


class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        super().__init__(loan, r, months)
        self.legend = f'Fixed, {r * 100:.1f}%'

class Fixed_with_pts(Mortgage):
    def __init__(self, loan, r, months, pts):
        super().__init__(loan, r, months)
        self.pts = pts
        self._paid = [loan * (pts/100)]
        self.legend = f'Fixed, {r * 100:.1f}%, {pts} pts'

class Two_rate(Mortgage):
    def __init__(self, loan, r, months, teaser_rate, teaser_months):
        super().__init__(loan, teaser_rate, months)
        self._teaser_months = teaser_months
        self._teaser_rate = teaser_rate
        self.next_rate = r/12
        self.legend = (f'{100 * teaser_rate:.1f}% for '  +
                        f'{self._teaser_months} months, then {100*r:.1f}%')
    
    def make_payment(self):
        if len(self._paid) == self._teaser_months + 1:
            self._rate = self.next_rate
            self._payment = find_payment(self._outstanding[-1], 
                                         self._rate,
                                         self._months -self._teaser_months)
        super().make_payment()

def find_payment(loan, r, m):
   """Assumes: loan and rare floats, m an int
       Returns the monthly payment for a mortage of
       size loan at monthly rate r for m months"""
   return loan * ((r *(1+r) ** m)/((1+r) ** m -1))

def compare_mortgages(amt, years, fixed_rate, pts, pts_rate, 
                      var_rate1, var_rate2, var_months):
    tot_months = years * 12
    fixed1 = Fixed(amt, fixed_rate, tot_months)
    fixed2 = Fixed_with_pts(amt, pts_rate, tot_months, pts)
    two_rate = Two_rate(amt, var_rate2, tot_months, var_rate1, var_months)
    morts = [fixed1, fixed2, two_rate]
    for m in range(tot_months):
        for mort in morts:
            mort.make_payment()
    plot_mortgages(morts, amt)


def plot_mortgages(morts, amt):
    def label_plot(figure, title, x_label, y_label):
        plt.figure(figure)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc = 'best')

    styles = ['k-', 'k-.', 'k:']
    payment, cost, balance, net_cost = 0, 1, 2, 3
    for i in range(len(morts)):
        plt.figure(payment)
        morts[i].plot_payments(styles[i])
        plt.figure(cost)
        morts[i].plot_tot_pd(styles[i])
        plt.figure(balance)
        morts[i].plot_balance(styles[i])
        plt.figure(net_cost)
        morts[i].plot_net(styles[i])

    label_plot(payment, f'Monthly Payments of ${amt:,} Mortages', 
               'Months', 'Monthly Payments')
    label_plot(cost, f'Cash outlay of ${amt:,} Mortages', 
               'Months', 'Total Payments')
    label_plot(balance, f'Balance Remaining of ${amt:,} Mortages', 
               'Months', 'Remaining Loan balance of $')
    label_plot(net_cost, f'Net Cost of ${amt:,} Mortages', 
               'Months', 'Payment - Equity $')

if __name__ == '__main__':
    compare_mortgages(amt=200000, years=30, fixed_rate=0.07,
                       pts = 3.25, pts_rate=0.05, var_rate1=0.045,
                       var_rate2=0.095, var_months=48)
    plt.show()
