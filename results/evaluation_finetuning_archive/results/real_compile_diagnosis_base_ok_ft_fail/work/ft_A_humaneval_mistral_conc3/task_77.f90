program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input from stdin
  read(*,*) a

  ! Call the iscube function
  result = iscube(a)

  ! Output the result
  print *, 'Output: ', result

contains

  logical function iscube(a)
    integer, intent(in) :: a
    integer :: root
    ! Check if a is a perfect cube
    if (a < 0) then
       root = -1
    else
       root = 0
    end if
    do while (root**3 < a)
       root = root + 1
    end do
    if (root**3 == a) then
       iscube = .true.
    else
       iscube = .false.
    end if
  end function iscube

end program iscube_demo