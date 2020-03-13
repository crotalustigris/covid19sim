SIMDAYS = 150           #SIMDAYS = # days to simulate
POP = 120e6             #POP = population


# Statistics to be plotted - each variable is an array of count for each day of simulation
UNINFECTEDBYDAY = []    #current number uninfected
CASESBYDAY = []         #current number infected not ended
INFECTIOUSBYDAY = []    #current number infectious
ENDEDBYDAY = []         #current number ended
SF = .19                #serious illness fraction

# simdays - number of days to simulate
# fraction_non_infections - those infected and immune but never infectious
# R0In - basic reproduction number. On any generation, new infections = R0*susceptible_population
def calculate(simdays, fraction_non_infectious, R0In, latency, contagious):
    global SIMDAYS, BYSTAGEDAY, UNINFECTEDBYDAY, CASESBYDAY, INFECTIOUSBYDAY, ENDEDBYDAY
    global MAXSYMP, WORSTDAY
    SIMDAYS = simdays                #Number of days to simulate
    I0 = 1000               #Initial number infected
    R0 = R0In               #Reproduction number - #infected by each case that become infectious
    L = latency                   #Mean Latency (time from infection until spreader0 in days
    CT = contagious                  #days contagious
    SF = .19                #SF = serious illness fraction
    #... China report 26FEB L:5-6, Recovery 14 days (not clear if infectious all that time)k
    L, CT, SF = 5, 8, .19
    #Counters
    INF, UNINF, E = 0, POP, 0     #I = Infectious, UNINF - Uninfected, E = Ended - not infectious or susceptible
    CUMINF = 1              #CUMINF - cumulate number infected
    MAXSYMP = I0            #MAXSYMP - max number of days symptomatic
    # Counts by day of infection - for staging  (L latency days, then CT contagious days)
    #   (not the same as counts by simulation day)
    initperday = I0/(L+CT)
    BYSTAGEDAY = [ ]
    for i in range(0, L + CT):
        BYSTAGEDAY.append(initperday)
        INF = INF + initperday

    UNINFECTEDBYDAY = []    #current number uninfected
    CASESBYDAY = []         #current number infected not ended
    INFECTIOUSBYDAY = []     #current number infectious
    ENDEDBYDAY = []         #current number ended

    print 'Latency:%d Contagious:%d Initial Inf:%d of %5d'%(L, CT, I0, POP)

    #Calculate - one day at a time, over full days range
    for d in range(0, SIMDAYS):
        # Reduce R0 based on how many are still available to infect
        R0adj = R0 * UNINF/POP
        R0NSadj = R0adj * fraction_non_infectious

        #Print a debugging line
        Dstr = '%3d:'%d       
        for i in range(0, L+CT):
            Dstr = '%s %8.3f'%(Dstr, BYSTAGEDAY[i])
        #print '%s CUMIN:%.1f R0adj:%.2f'%(Dstr, CUMINF, R0adj)


        NEW = list(BYSTAGEDAY)        #Create a staging list from the current

        # Calculate number of new infections, and number currently infectious
        newInf, newNS, infectious = 0, 0, 0
        for i in range(L-1, L+CT):    #Make new infections
            newInf = newInf + BYSTAGEDAY[i]*R0adj/CT
            newNS = newNS + BYSTAGEDAY[i]*R0NSadj/CT
            infectious = infectious + BYSTAGEDAY[i]
        # Update master counters 
        ending = BYSTAGEDAY[L+CT-1]
        UNINF = UNINF - newInf - newNS              # Subtract new infections from uninfected 
        INF = INF + newInf - ending         # Calc num infectious by adding new, subtracting ended
        E = E + ending + newNS              # Calc number ended (no longer infectious)
        if MAXSYMP < infectious:            #Max symptomatic (same as infectious)
            MAXSYMP = infectious
            WORSTDAY = d + 1
        CUMINF = CUMINF + newInf            # Update cumulative infected count
        #print '%4d: newInf:%7d newNS:%7d Uninf:%12d'%(d, newInf, newNS, UNINF)

        # Now update the new staging list by
        #  using new infection rate for day 0, and shifting other days forward in list
        NEW[0] = newInf
        for i in range(0, L+CT):
            if i > 0:
                NEW[i] = BYSTAGEDAY[i-1]
        #if d%7 == 0 and d > 0:
        #    print 'end of wk:%3d cases/1000:%12d'%(d/7+1, CASESBYDAY[d-1])

        BYSTAGEDAY = NEW

        #Update the by-day lists - for plotting
        CASESBYDAY.append(INF)
        print 'day:%3d newInf:%d newNS:%d ending:%d infectious:%12d'%(d, newInf, newNS, ending, INF)
        UNINFECTEDBYDAY.append(UNINF)
        ENDEDBYDAY.append(E)
        INFECTIOUSBYDAY.append(infectious)

#
# Plotting Section - import standard libraries
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
import numpy as np
import matplotlib.pyplot as plt

# Function to create one subplot - called with:
# fig - the figure to plot inside of
# subplotIII - the subplot location information
def do_subplot(fig, subplotIII, typestr, scale):
    global POP, UNINFECTEDBYDAY, CASESBYDAY, ENDEDBYDAY, INFECTIOUSBYDAY, SIMDAYS, WORSTDAY

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    # A grid of time points (in days) - first scale the arrays
    UNINF = [ x/scale for x in UNINFECTEDBYDAY ]
    INF = [ x/scale for x in CASESBYDAY ]
    ENDED = [ x/scale for x in ENDEDBYDAY ]
    INFECTIOUS = [ x/scale for x in INFECTIOUSBYDAY ]

    t = np.linspace(0, SIMDAYS, SIMDAYS)
    ax = fig.add_subplot(subplotIII, axis_bgcolor='#dddddd', axisbelow=True)
    #ax.plot(t, UNINF, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, UNINF, 'y', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, INF, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, INFECTIOUS, 'b', alpha=0.5, lw=2, label='Infectious')
    ax.plot(t, ENDED, 'g', alpha=0.5, lw=2, label='Post-Infection')
    ax.set_xlabel(typestr + ' - Days')
    ax.set_ylabel('Cases in %d\'s'%scale)
    ax.set_ylim(0,100)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    # place a text box in upper left in axes coords
    # ...these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    MSYMPf = locale.format("%d", MAXSYMP, grouping=True)
    MSERf = locale.format("%d", MAXSYMP*SF, grouping=True)
    label = ' WORST DAY %d\r\nSymptomatic:%s\nSeriously Ill:  %s'% (WORSTDAY, MSYMPf, MSERf)
    ax.text(0.05, 0.7, label, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)


#  MAIN LINE OF PROGRAM
ND=500 #Number of days
PLOTSCALE=1e6
fig = plt.figure(facecolor='w')
calculate(ND, 0, 2.3, 5, 10)            #Do it for zero non-infectious (percentage)
do_subplot(fig, 121, "R0 2.3", PLOTSCALE)
calculate(ND, .49, 1.1, 5, 10)          #Do it for non-zero non-infections (percentage)
do_subplot(fig, 122, "R0 1.1", PLOTSCALE)

plt.show()
