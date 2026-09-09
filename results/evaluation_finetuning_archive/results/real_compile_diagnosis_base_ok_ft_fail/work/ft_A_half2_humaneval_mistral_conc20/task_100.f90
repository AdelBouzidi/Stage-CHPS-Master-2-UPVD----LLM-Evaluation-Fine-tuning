program main
    implicit none
    integer :: n
    integer, allocatable :: pile(:)
    
    read(*,*) n
    call make_a_pile(n, pile)
    write(*,*) pile
end program main