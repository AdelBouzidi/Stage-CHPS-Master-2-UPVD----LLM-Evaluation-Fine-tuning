program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read(*,*) a

  ! Call the function
  result = iscube(a)

  ! Output result
  print *, result

contains

  function iscube(a) result(res)
    implicit none
    integer, intent(in) :: a
    logical :: res
    integer :: i

    res = .false.
    do i = 1, 1000
      if (i**3 == a) then
        res = .true.
        exit
      end if
    end do
  end function iscube

end program iscube_demo