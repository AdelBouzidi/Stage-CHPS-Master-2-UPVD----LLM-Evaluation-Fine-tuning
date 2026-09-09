program iscube
    implicit none
    integer :: a
    integer :: root
    integer :: n
    logical :: result
    
    read(*,*) a
    
    if (a < 0) then
        n = -a
        root = int(n**(1.0/3.0))
        if (root**3 == n) then
            result = .true.
        else
            result = .false.
        end if
    else
        root = int(a**(1.0/3.0))
        if (root**3 == a) then
            result = .true.
        else
            result = .false.
        end if
    end if
    
    print *, result
end program iscube