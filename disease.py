import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def simulation(fixed, variable):
    """
    Simulate epidemic spread with variable social distancing parameters.
    
    Parameters:
        fixed (dict): Fixed simulation parameters
        variable (dict): Social distancing parameters that can be adjusted
    Returns:
        tuple: (daily infections list, total infections, peak infections, peak day)
    """
    infected = [fixed['initial_infections']]
    new_infections = [fixed['initial_infections']]
    total_infections = fixed['initial_infections']
    peak_infections = fixed['initial_infections']
    peak_day = 0

    for t in range(fixed['duration']):
        cur_infections = infected[-1]
        if len(new_infections) > fixed['days_spreading']:
            cur_infections -= new_infections[-fixed['days_spreading'] -1]
            
        daily_contacts = (variable['red_daily_contacts'] 
                         if t >= variable['red_start'] and t < variable['red_end']
                         else fixed['init_contacts'])
                         
        total_contacts = cur_infections * daily_contacts
        susceptible = fixed['pop'] - total_infections
        risky_contacts = total_contacts * (susceptible/fixed['pop'])
        newly_infected = round(risky_contacts * fixed['contagiousness'])
        
        new_infections.append(newly_infected)
        total_infections += newly_infected
        infected.append(cur_infections + newly_infected)
        
        if infected[-1] > peak_infections:
            peak_infections = infected[-1]
            peak_day = t

    return infected, total_infections, peak_infections, peak_day

def plot_infections(infections, total_infections, peak_infections, peak_day, fixed, variable):
    """
    Create enhanced visualization of the epidemic simulation.
    """
    plt.cla()  # Clear previous plot
    
    # Plot main infection curve
    infection_plot = plt.plot(infections, 'r', label='Active Infections', linewidth=2)[0]
    
    # Add social distancing period visualization
    plt.axvspan(variable['red_start'], variable['red_end'], 
                alpha=0.2, color='gray', label='Social Distancing Period')
    
    # Add peak marker
    plt.plot(peak_day, peak_infections, 'ro', markersize=10, label='Peak')
    
    # Customize appearance
    plt.grid(True, alpha=0.3)
    plt.xticks(np.arange(0, fixed['duration']+1, 50), fontsize='large')
    plt.yticks(fontsize='large')
    plt.xlabel('Days Since First Infection', fontsize='xx-large')
    plt.ylabel('Number Currently Infected', fontsize='xx-large')
    
    # Create detailed title
    reduction = (1 - variable['red_daily_contacts']/fixed['init_contacts']) * 100
    title = (f'Interactive Epidemic Simulation\n'
             f"Population: {fixed['pop']:,} | "
             f"Base Contacts/Day: {fixed['init_contacts']} | "
             f"Infectivity: {(100 * fixed['contagiousness']):.1f}%\n"
             f"Contact Reduction: {reduction:.0f}%")
    plt.title(title, fontsize='xx-large', pad=20)
    
    # Add statistics text box
    stats_text = (
        f'Peak infections: {peak_infections:,.0f}\n'
        f'Peak occurs on day: {peak_day}\n'
        f'Total infections: {total_infections:,.0f}\n'
        f'Percent infected: {(total_infections/fixed["pop"]*100):.1f}%'
    )
    txt_box = plt.text(0.02, 0.98, stats_text,
                      transform=plt.gca().transAxes,
                      verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                      fontsize='large')
    
    plt.legend(fontsize='large', loc='center right')
    return infection_plot, txt_box

def update(val, fixed, axes_dict):
    """
    Update the simulation based on slider values.
    """
    variable = {
        'red_daily_contacts': axes_dict['contact_slider'].val,
        'red_start': int(axes_dict['start_slider'].val),
        'red_end': int(axes_dict['end_slider'].val)
    }
    
    infections, total_infections, peak_infections, peak_day = simulation(fixed, variable)
    
    plt.sca(axes_dict['infections_ax'])
    plot_infections(infections, total_infections, peak_infections, peak_day, fixed, variable)
    plt.draw()

def create_simulation_gui():
    """
    Create the interactive simulation interface with sliders.
    """
    fixed = {
        'pop': 5000000,          # population at risk
        'duration': 500,         # number of days
        'initial_infections': 4,  # initial number of cases
        'init_contacts': 50,     # contacts without social distancing
        'contagiousness': 0.005, # prob. of getting disease if exposed
        'days_spreading': 10     # days contagious after infection
    }
    
    variable = {
        'red_daily_contacts': 35,
        'red_start': 20,
        'red_end': 200
    }
    
    # Create figure and axis layout
    fig = plt.figure(figsize=(14, 10))
    
    # Create axes for plots and sliders
    axes_dict = {
        'infections_ax': plt.axes([0.12, 0.25, 0.8, 0.65]),
        'contact_slider': Slider(
            plt.axes([0.25, 0.12, 0.65, 0.03]),
            'Contacts/Day\nDuring Distancing',
            0, fixed['init_contacts'],
            variable['red_daily_contacts']
        ),
        'start_slider': Slider(
            plt.axes([0.25, 0.08, 0.65, 0.03]),
            'Start Day of\nDistancing',
            1, 30,
            variable['red_start']
        ),
        'end_slider': Slider(
            plt.axes([0.25, 0.04, 0.65, 0.03]),
            'End Day of\nDistancing',
            30, 400,
            variable['red_end']
        )
    }
    
    # Style the sliders
    for slider in [axes_dict['contact_slider'], 
                  axes_dict['start_slider'], 
                  axes_dict['end_slider']]:
        slider.label.set_fontsize(12)
        slider.valtext.set_fontsize(12)
    
    # Initial plot
    infections, total_infections, peak_infections, peak_day = simulation(fixed, variable)
    plt.sca(axes_dict['infections_ax'])
    plot_infections(infections, total_infections, peak_infections, peak_day, fixed, variable)
    
    # Connect sliders to update function
    update_func = lambda val: update(val, fixed, axes_dict)
    axes_dict['contact_slider'].on_changed(update_func)
    axes_dict['start_slider'].on_changed(update_func)
    axes_dict['end_slider'].on_changed(update_func)
    
    plt.show()

if __name__ == "__main__":
    create_simulation_gui()