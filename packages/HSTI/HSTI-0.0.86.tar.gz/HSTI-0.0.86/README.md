This package contains functions used in data processing of hyperspectral images
captured using a scanning Fabry-Pérot interferometer (FPI). This includes transmission
simulations of the FPI itself.

-------------------

Key Features:

* **Image importing**

* **Most common image analysis**

* **Fabry-Pérot simulation**



## Quick Start


1. **Installation** - Run `pip3 install HSTI`.


2. **Adding Examples in a Jupyter notebook or .py file**

        import HSTI

3. **Importing a hyperspectral image**

        path = '/home/user/experiments/experiment_1'

        HS_image = HSTI.import_data_cube(path)

4. **Performing a PCA of the hyperspectral image**

        PCA_object = HSTI.PCA()

        #transform image to two-dimensional
        two_dim = np.reshape(HS_image,(HS_image.shape[0]*HS_image.shape[1],HS_image.shape[2]))

        #calculate and apply PCA
        PCA_object.calculate_pca(two_dim)
        PCA_two_dim_imgs = PCA_object.apply_pca(two_dim)

        #create three-dimensional datacube with PCA images
        pca_imgs = np.reshape(PCA_two_dim_imgs,(HS_image.shape[0],HS_image.shape[1],HS_image.shape[2]))


5. **Visualising the principal components**

        #import string for labelling images
        import string

        fig,ax = plt.subplots(4,4,figsize=(14,16.0))

        newtec_cm = HSTI.import_cm()

        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('axes', labelsize=10)
        plt.rc('lines', linewidth=2)
        plt.rc('legend', fontsize=8)
        plt.rc('figure', titlesize=10)
        plt.rc('axes', titlesize=10)

        axs = ax.flat

        for idx,ax in enumerate(axs):

        _std = np.std(pca_imgs[:,:,idx])
        _mean = np.mean(pca_imgs[:,:,idx])

        if idx < 16:
        im = ax.imshow(pca_imgs[:,:,idx],vmin = _mean-2*_std,vmax = _mean+2*_std, cmap=newtec_cm)
        ax.text(0.5, 0.92, 'PC' + str(idx+1), transform=ax.transAxes,
            size=12, weight='bold', horizontalalignment='center',color='white')

        ax.text(0.02, 0.92,'(' + string.ascii_uppercase[idx] + ')', transform=ax.transAxes,
        size=10, weight='bold',color='white')

        if idx == 0 or idx == 4 or idx == 8 or idx == 12:
        ax.set_ylabel('Y [y$_j$]')

        if idx > 11:
        ax.set_xlabel('X [x$_i$]')


        plt.tight_layout()
        plt.savefig('experiment_1' + '_PCA' + '.png', dpi=100, bbox_inches='tight')


6. **Simulating the Fabry-Pérot transmission**

        data_ac = np.loadtxt('NO.csv', delimiter=',')

        lam_ac = data_ac[:,0] #[µm]
        idx = ((lam_ac < 17) & (lam_ac > 7))

        lam_ac = lam_ac[idx]
        spec_ac = data_ac[idx,1]

        diff_lam_ac = np.diff(lam_ac)
        diff_lam_ac = np.append(diff_lam_ac, diff_lam_ac[-1])

        t = np.zeros(len(lam_ac)) #Transmittance of FPI
        r = np.zeros(len(lam_ac)) #Reflectance of FPI
        l = np.zeros(len(lam_ac)) #Numeric loss

        A_ac = np.zeros([len(mirror_sep_ac), len(lam_ac)])



        with open('interpolatedResponse.pkl', 'rb') as f:
        interpolate_resp = pickle.load(f)



        resp = np.zeros([len(lam_ac)])
        for i in range(len(lam_ac)):
        resp[i] = interpolate_resp(lam_ac[i]*1e-6)



        for i in range(len(mirror_sep_ac)):
        clear_output(wait=True)
        print('Progress: ' + str(np.round(100*(i+1)/len(mirror_sep_ac), decimals = 2)) + '%')
        for j in range(len(lam_ac)):
        t[j], r[j], l[j] = FPI_trans(mirror_sep_ac[i]*1e-6, lam_ac[j]/1e6, 297)
        t[j] = t[j]*(-diff_lam_ac[j])
        A_ac[i,:] = t*spec_ac



        sim_spec_ac = A_ac@resp
        sim_spec_ac = sim_spec_ac - np.min(sim_spec_ac)
        sim_spec_ac = sim_spec_ac/np.max(sim_spec_ac)



        fig8 = plt.figure()
        fig8.set_figheight(5) #set height of the entire figure
        fig8.set_figwidth(10) #set width of the entire figure
        gs = gridspec.GridSpec(1, 2) #set size ratio of the subfigures
        ax1 = fig8.add_subplot(gs[0,0])
        ax2 = fig8.add_subplot(gs[0,1])



        ax1.plot(mirror_sep_ac, sim_spec_ac, color = 'blue', label = 'Simulated')
        ax1.plot(mirror_sep_ac, meas_spec_ac, color = 'red', label = 'Measured')
        ax1.grid()
        ax1.legend()
        ax1.set_xlabel('Mirror separation [µm]')
        ax1.set_ylabel('Intensity [a.u.]')



        ax2.plot(lam_ac, spec_ac)
        ax2.grid()
        ax2.set_xlabel('Wavelength [µm]')
        ax2.set_ylabel('Intensity [a.u.]')
        fig8.tight_layout(pad = 2)



        sim_spec_ac_meth = sim_spec_ac



-------------------
# Contact

  *For bug reports or other questions please contact mani@newtec.dk or alj@newtec.dk.*
